# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/cmb/Workspace/FR24_Analyzer/FR24Analyzer/UI/FR24Analyzer.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 646)
        MainWindow.setMinimumSize(QtCore.QSize(680, 646))
        MainWindow.setMaximumSize(QtCore.QSize(680, 646))
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.configureButton = QtWidgets.QPushButton(self.centralwidget)
        self.configureButton.setGeometry(QtCore.QRect(590, 10, 75, 25))
        self.configureButton.setObjectName("configureButton")
        self.dbTable = QtWidgets.QTableWidget(self.centralwidget)
        self.dbTable.setGeometry(QtCore.QRect(10, 10, 571, 411))
        self.dbTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.dbTable.setObjectName("dbTable")
        self.dbTable.setColumnCount(0)
        self.dbTable.setRowCount(0)
        self.dbTable.horizontalHeader().setCascadingSectionResizes(False)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 460, 571, 141))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.textEdit = QtWidgets.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(350, 10, 211, 121))
        self.textEdit.setObjectName("textEdit")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 326, 109))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout_3.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.predFlight = QtWidgets.QTextEdit(self.layoutWidget)
        self.predFlight.setMinimumSize(QtCore.QSize(161, 31))
        self.predFlight.setMaximumSize(QtCore.QSize(161, 31))
        self.predFlight.setObjectName("predFlight")
        self.verticalLayout_2.addWidget(self.predFlight)
        self.predApproach = QtWidgets.QTextEdit(self.layoutWidget)
        self.predApproach.setMinimumSize(QtCore.QSize(161, 31))
        self.predApproach.setMaximumSize(QtCore.QSize(161, 31))
        self.predApproach.setObjectName("predApproach")
        self.verticalLayout_2.addWidget(self.predApproach)
        self.actApproach = QtWidgets.QTextEdit(self.layoutWidget)
        self.actApproach.setMinimumSize(QtCore.QSize(161, 31))
        self.actApproach.setMaximumSize(QtCore.QSize(161, 31))
        self.actApproach.setObjectName("actApproach")
        self.verticalLayout_2.addWidget(self.actApproach)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.rowCount = QtWidgets.QLabel(self.centralwidget)
        self.rowCount.setGeometry(QtCore.QRect(426, 430, 151, 20))
        self.rowCount.setText("")
        self.rowCount.setObjectName("rowCount")
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(590, 510, 77, 89))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.getButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.getButton.setObjectName("getButton")
        self.verticalLayout.addWidget(self.getButton)
        self.fitButton = QtWidgets.QPushButton(self.layoutWidget1)
        self.fitButton.setObjectName("fitButton")
        self.verticalLayout.addWidget(self.fitButton)
        self.getButton_3 = QtWidgets.QPushButton(self.layoutWidget1)
        self.getButton_3.setObjectName("getButton_3")
        self.verticalLayout.addWidget(self.getButton_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 680, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FR24 Analyzer"))
        self.configureButton.setText(_translate("MainWindow", "Configure"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Data Units:</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Altitude - Feet</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Speed - Knots</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Distance - Kilometers</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Approach Time - Seconds</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label.setText(_translate("MainWindow", "Flight"))
        self.label_2.setText(_translate("MainWindow", "Predicted Approach Time"))
        self.label_3.setText(_translate("MainWindow", "Actual Approach Time"))
        self.getButton.setText(_translate("MainWindow", "GET"))
        self.fitButton.setText(_translate("MainWindow", "FIT"))
        self.getButton_3.setText(_translate("MainWindow", "RUN"))
