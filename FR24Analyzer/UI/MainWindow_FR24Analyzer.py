#! /usr/bin/env python3

import sys, os, time
from FR24Analyzer.UI.Ui_FR24Analyzer import Ui_MainWindow
from FR24Analyzer.UI.ConfigureWindow_FR24Analyzer import ConfigureDialog
from FR24Analyzer.store.store import PostGreSQL
from FR24Analyzer import FR24Analyzer

from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QObject, QSettings, QItemSelection, QMimeData, QCoreApplication
from PyQt5.QtGui import QFont, QIcon, QMovie, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QAbstractItemView, QAction, QApplication, QFrame, QLabel, QMainWindow, QMenu, QTableWidgetItem, QWidget, QDialog

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.font = QFont("Arial", 10, QFont.Serif)

        #Main Window signals
        self.ui.configureButton.pressed.connect(self.showConfigure)
        self.ui.getButton.pressed.connect(self.showData)

        #Model Class
        self.model = PostGreSQL()
    
    def showData(self):
        data = self.model.getFromDB()
        rowCount = len(data[1][:])
        columnCount = len(data[:][1])
        self.ui.dbTable.setFont(self.font);
        self.ui.dbTable.setRowCount(rowCount);
        self.ui.dbTable.setColumnCount(columnCount);
        self.ui.dbTable.setHorizontalHeaderLabels(str("Flight;Lattitude;Longtitude;Heading;Altitude;Speed;ApproachTime;Distance").split(";"))
        for row in range(0,rowCount):
            for column in range(0,columnCount):
                self.ui.dbTable.setItem(row, column, QTableWidgetItem(str(data[row][column])))
        self.ui.dbTable.resizeColumnsToContents()
    
    def showConfigure(self):
        self.configureDialog = ConfigureDialog()
        ret = self.configureDialog.show()
        print(ret)
        # configureDialog = QDialog(self.ui.centralwidget)
        # configureDialog.open()

    

def main():
    app = QApplication(sys.argv)
    client = Window()
    client.show()
    sys.exit(app.exec_())


