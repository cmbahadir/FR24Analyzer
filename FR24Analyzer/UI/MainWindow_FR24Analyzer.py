#! /usr/bin/env python3

import sys, os, time
from FR24Analyzer.UI.Ui_FR24Analyzer import Ui_MainWindow
from FR24Analyzer.store.store import PostGreSQL
from FR24Analyzer import FR24Analyzer

from PyQt5.QtCore import pyqtSignal, QTimer, Qt, QObject, QSettings, QItemSelection, QMimeData, QCoreApplication
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QMovie
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QAbstractItemView, QMenu, QAction, QFrame, QLabel

class Window(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.pressed.connect(self.collectData)

        self.model = PostGreSQL()
    
    def collectData(self):
        # gifpath = os.path.join("Elements", "loading.gif")
        # self.loading = QMovie(gifpath)
        # movie = QMovie("loading.gif")
        # self.ui.statusLabel.setMovie(movie)
        # movie.start()
        # self.ui.gridLayout.addWidget(self.ui.statusLabel)
        self.ui.statusLabel.setText("Started to collect data.")
        analyzer = FR24Analyzer.FR24Analyzer(logging=False)
        while True:
            analyzer.getLandingTimeToAirport()
            time.sleep(2)
            records = self.model.getFromDB()
            self.ui.statusLabel.setText(str(len(records)))

def main():
    app = QApplication(sys.argv)
    client = Window()
    client.show()
    sys.exit(app.exec_())


