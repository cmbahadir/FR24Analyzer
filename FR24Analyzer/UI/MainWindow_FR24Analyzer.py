#! /usr/bin/env python3
import sys, os, time, subprocess

from FR24Analyzer.UI.Ui_FR24Analyzer import Ui_MainWindow
from FR24Analyzer.UI.ConfigureWindow_FR24Analyzer import ConfigureDialog
from FR24Analyzer.store.store import PostGreSQL
from FR24Analyzer import FR24Analyzer
from FR24Analyzer.fit import fit

from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QFont, QStandardItemModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QTableWidgetItem, QWidget, QDialog

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.font = QFont("Arial", 10, QFont.Serif)

        #Main Window signals
        self.ui.configureButton.pressed.connect(self.showConfigure)
        self.ui.getButton.pressed.connect(self.runGET)
        self.ui.fitButton.pressed.connect(self.runFIT)

        #Model Class
        model = PostGreSQL()
        self.data = model.getFromDB()
        self.showData()
    
    def showData(self, highlight=None):
        self.rowCount = len(self.data)
        self.columnCount = len(self.data[:][1])
        self.ui.rowCount.setText("Number of Rows: " + str(self.rowCount))
        self.ui.dbTable.setFont(self.font)
        self.ui.dbTable.setRowCount(self.rowCount)
        self.ui.dbTable.setColumnCount(self.columnCount)
        self.ui.dbTable.setHorizontalHeaderLabels(str("Flight;Lattitude;Longtitude;Heading;Altitude;Speed;Approach Time;Distance").split(";"))
        for row in range(0,self.rowCount):
            if highlight != None and str(self.data[row][0]) == highlight:
                self.ui.dbTable.selectRow(row)
            for column in range(0,self.columnCount):
                self.ui.dbTable.setItem(row, column, QTableWidgetItem(str(self.data[row][column])))
                

        self.ui.dbTable.resizeColumnsToContents()
    
    def showConfigure(self):
        self.configureDialog = ConfigureDialog()
        ret = self.configureDialog.show()
    
    ## GET BUTTON
    def runGET(self):
        self.ui.getButton.setText("Running")
        command = "python3"
        args = ["fr24Analyzer.py","--g","GET"]
        self.process = QProcess(self)
        self.process.finished.connect(self.onFinished)
        self.process.startDetached(command, args)
        self.ui.getButton.pressed.connect(self.stopGET)
    
    def stopGET(self):
        #TODO: Only reason why this program works only on Linux
        getPIDLinux = '$(ps -fu $USER | grep "GET" | grep "fr24Analyzer.py" | grep -v "grep" | awk \'{print $2}\')'
        subprocess.call("kill -9 " + getPIDLinux, shell=True)
        self.ui.getButton.setText("GET")
        self.ui.getButton.pressed.connect(self.runGET)

    def onFinished(self, exitCode, exitStatus):
        self.ui.getButton.setText("GET")
    
    ## FIT BUTTON
    def runFIT(self):
        fitter = fit.Fit()
        fittedResult = fitter.fitData()
        self.showData(highlight=fittedResult[0])
        self.ui.predFlight.setText(fittedResult[0])
        self.ui.actApproach.setText(fittedResult[1])
        self.ui.predApproach.setText(fittedResult[2])

def main():
    app = QApplication(sys.argv)
    client = Window()
    client.show()
    sys.exit(app.exec_())


