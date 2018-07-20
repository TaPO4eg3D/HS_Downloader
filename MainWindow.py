# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui',
# licensing of 'MainWindow.ui' applies.
#
# Created: Fri Jul 20 14:29:59 2018
#      by: pyside2-uic  running on PySide2 5.11.1a1.dev1530005708
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(475, 263)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.searchButton = QtWidgets.QPushButton(self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(340, 10, 121, 31))
        self.searchButton.setObjectName("searchButton")
        self.selectAll = QtWidgets.QPushButton(self.centralwidget)
        self.selectAll.setGeometry(QtCore.QRect(340, 55, 121, 31))
        self.selectAll.setObjectName("selectAll")
        self.deselectAll = QtWidgets.QPushButton(self.centralwidget)
        self.deselectAll.setGeometry(QtCore.QRect(340, 90, 121, 31))
        self.deselectAll.setObjectName("deselectAll")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(340, 50, 118, 3))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.downloadButton = QtWidgets.QPushButton(self.centralwidget)
        self.downloadButton.setGeometry(QtCore.QRect(340, 220, 121, 31))
        self.downloadButton.setObjectName("downloadButton")
        self.animeView = QtWidgets.QListWidget(self.centralwidget)
        self.animeView.setGeometry(QtCore.QRect(10, 50, 321, 201))
        self.animeView.setObjectName("animeView")
        self.searchField = QtWidgets.QLineEdit(self.centralwidget)
        self.searchField.setGeometry(QtCore.QRect(10, 10, 321, 31))
        self.searchField.setObjectName("searchField")
        self.loadingStatus = QtWidgets.QLabel(self.centralwidget)
        self.loadingStatus.setEnabled(True)
        self.loadingStatus.setGeometry(QtCore.QRect(340, 160, 121, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        font.setWeight(75)
        font.setBold(True)
        self.loadingStatus.setFont(font)
        self.loadingStatus.setAlignment(QtCore.Qt.AlignCenter)
        self.loadingStatus.setObjectName("loadingStatus")
        self.selectQuality = QtWidgets.QComboBox(self.centralwidget)
        self.selectQuality.setGeometry(QtCore.QRect(340, 190, 121, 22))
        self.selectQuality.setObjectName("selectQuality")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "HS: Downloader", None, -1))
        self.searchButton.setText(QtWidgets.QApplication.translate("MainWindow", "Search", None, -1))
        self.selectAll.setText(QtWidgets.QApplication.translate("MainWindow", "Select all", None, -1))
        self.deselectAll.setText(QtWidgets.QApplication.translate("MainWindow", "Deselect all", None, -1))
        self.downloadButton.setText(QtWidgets.QApplication.translate("MainWindow", "Download", None, -1))
        self.loadingStatus.setText(QtWidgets.QApplication.translate("MainWindow", "Loading...", None, -1))

