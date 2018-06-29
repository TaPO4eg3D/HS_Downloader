# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui',
# licensing of 'MainWindow.ui' applies.
#
# Created: Fri Jun 29 15:35:34 2018
#      by: pyside2-uic  running on PySide2 5.11.1a1.dev1530005708
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(473, 265)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.animeView = QtWidgets.QTableView(self.centralwidget)
        self.animeView.setGeometry(QtCore.QRect(10, 51, 321, 201))
        self.animeView.setObjectName("animeView")
        self.searchField = QtWidgets.QTextEdit(self.centralwidget)
        self.searchField.setGeometry(QtCore.QRect(10, 10, 321, 31))
        self.searchField.setObjectName("searchField")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(340, 10, 121, 41))
        self.searchButton.setObjectName("searchButton")
        self.selectAll = QtWidgets.QPushButton(self.centralwidget)
        self.selectAll.setGeometry(QtCore.QRect(340, 70, 121, 31))
        self.selectAll.setObjectName("selectAll")
        self.deselectAll = QtWidgets.QPushButton(self.centralwidget)
        self.deselectAll.setGeometry(QtCore.QRect(340, 105, 121, 31))
        self.deselectAll.setObjectName("deselectAll")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(340, 60, 118, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.downloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadButton.setGeometry(QtCore.QRect(340, 220, 121, 31))
        self.downloadButton.setObjectName("downloadButton")
        self.downloadButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.downloadButton_2.setGeometry(QtCore.QRect(340, 185, 121, 31))
        self.downloadButton_2.setObjectName("downloadButton_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "HS: Downloader", None, -1))
        self.searchField.setToolTip(QtWidgets.QApplication.translate("MainWindow", "Insert here the name of anime", None, -1))
        self.searchButton.setText(QtWidgets.QApplication.translate("MainWindow", "Search", None, -1))
        self.selectAll.setText(QtWidgets.QApplication.translate("MainWindow", "Select all", None, -1))
        self.deselectAll.setText(QtWidgets.QApplication.translate("MainWindow", "Deselect all", None, -1))
        self.downloadButton.setText(QtWidgets.QApplication.translate("MainWindow", "Download", None, -1))
        self.downloadButton_2.setText(QtWidgets.QApplication.translate("MainWindow", "Display episodes", None, -1))

