# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guidesign_4.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(974, 777)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.btnStart = QtWidgets.QPushButton(self.centralwidget)
        self.btnStart.setObjectName("btnStart")
        self.horizontalLayout_5.addWidget(self.btnStart)
        self.btnStop = QtWidgets.QPushButton(self.centralwidget)
        self.btnStop.setObjectName("btnStop")
        self.horizontalLayout_5.addWidget(self.btnStop)
        self.checkDebug = QtWidgets.QCheckBox(self.centralwidget)
        self.checkDebug.setObjectName("checkDebug")
        self.horizontalLayout_5.addWidget(self.checkDebug)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.verticalLayout_2.addWidget(self.treeWidget)
        self.horizontalLayout_6.addLayout(self.verticalLayout_2)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.horizontalLayout_6.addWidget(self.tableWidget)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnStart.setText(_translate("MainWindow", "Start"))
        #MainWindow.setWindowIcon(QIcon('modbus.png'))
        self.btnStop.setText(_translate("MainWindow", "Stop"))
        self.checkDebug.setText(_translate("MainWindow", "Debug"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "mbrecords"))

