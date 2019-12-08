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
        self.configureParameters = self.configureHelper.readFromConfigFile("config.yaml")
        if self.configureParameters != False:
            self.configureDialog.airportLat.setText(str(self.configureParameters['airportLat']))
            self.configureDialog.airportLon.setText(str(self.configureParameters['airportLon']))
            self.configureDialog.airportName.setText(str(self.configureParameters['airportName']))
            self.configureDialog.areaLat.setText(str(self.configureParameters['bounds']).split(',')[0])
            self.configureDialog.areaLon.setText(str(self.configureParameters['bounds']).split(',')[1])
            self.configureDialog.redisIP.setText(str(self.configureParameters['redis_ip']))
            self.configureDialog.postgresIP.setText(str(self.configureParameters['postgres_ip']))
        
        self.configureDialog.configureBrowseButton.pressed.connect(self.browseMethod)
        print("Debug")
    
    def browseMethod(self):
        browseDialog = QFileDialog(self)
        browseDialog.open()
        configFilename = browseDialog.getOpenFileName()
        browseDialog.close()
        print(configFilename)

