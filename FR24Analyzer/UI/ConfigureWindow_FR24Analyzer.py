#! /usr/bin/env python3

import sys, os, time
from FR24Analyzer.UI.Ui_FR24Analyzer import Ui_MainWindow
from FR24Analyzer.UI.Ui_configureDialog import Ui_configureDialog
from FR24Analyzer.helper.helper import Helper
from FR24Analyzer.store.store import PostGreSQL
from FR24Analyzer import FR24Analyzer

from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QObject, QSettings, QItemSelection, QMimeData, QCoreApplication
from PyQt5.QtGui import QFont, QIcon, QMovie, QStandardItem, QStandardItemModel
from PyQt5.QtWidgets import QAbstractItemView, QAction, QApplication, QFrame, QLabel, QMainWindow, QMenu, QTableWidgetItem, QWidget, QDialog, QFileDialog
from PyQt5 import QtCore

class ConfigureDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.configureDialog = Ui_configureDialog()
        self.configureDialog.setupUi(self)
        
        #Get from Model
        self.configureHelper = Helper()
        #TODO: Change to config.yaml after right formatting of the saved file.
        self.configureParameters = self.configureHelper.readFromConfigFile("config.yaml")
        if self.configureParameters != False:
            self.configureDialog.airportLat.setText(str(self.configureParameters['airportLat']))
            self.configureDialog.airportLon.setText(str(self.configureParameters['airportLon']))
            self.configureDialog.airportName.setText(str(self.configureParameters['airportName']))
            self.configureDialog.areaLat.setText(str(self.configureParameters['bounds']).split(',')[0]+ ',' + str(self.configureParameters['bounds']).split(',')[1])
            self.configureDialog.areaLon.setText(str(self.configureParameters['bounds']).split(',')[2]+ ',' + str(self.configureParameters['bounds']).split(',')[3])
            self.configureDialog.redisIP.setText(str(self.configureParameters['redis_ip']) + ":" + str(self.configureParameters['redis_port']))
            self.configureDialog.postgresIP.setText(str(self.configureParameters['postgres_ip']) + ":" + str(self.configureParameters['postgres_port']))
        
        self.configureDialog.configureBrowseButton.pressed.connect(self.browseMethod)
        self.configureDialog.saveConfig.pressed.connect(self.saveConfiguration)
    
    def browseMethod(self):
        browseDialog = QFileDialog(self)
        browseDialog.open()
        configFilename = browseDialog.getOpenFileName()
        browseDialog.close()
        print(configFilename)
    
    def saveConfiguration(self):
        self.userParameters = dict()
        #TODO: Set a type and range restriction for each field.
        self.userParameters['airportLat']=self.configureDialog.airportLat.toPlainText()
        self.userParameters['airportLon']=self.configureDialog.airportLon.toPlainText()
        self.userParameters['airportName']=self.configureDialog.airportName.toPlainText()
        self.userParameters['redis_ip']=self.configureDialog.redisIP.toPlainText().split(':')[0]
        self.userParameters['redis_port']=self.configureDialog.redisIP.toPlainText().split(':')[1]
        self.userParameters['postgres_ip']=self.configureDialog.postgresIP.toPlainText().split(':')[0]
        self.userParameters['postgres_port']=self.configureDialog.postgresIP.toPlainText().split(':')[1]
        self.userParameters['bounds']=self.configureDialog.areaLat.toPlainText() + "," + self.configureDialog.areaLon.toPlainText()
        self.configureHelper.writeToConfigFile("config.yaml", self.userParameters)

