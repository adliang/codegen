from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidget,QTableWidgetItem
import guidesign
import sys
import os
from time import sleep
import threading
from tkinter import *
import tkinter.messagebox
import time
import random
import _thread
import win_inet_pton
import socket
from pyModbusTCP.client import ModbusClient
import json
from pprint import pprint
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QTreeView

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 502
#192.168.1.78
# TODO make length of poll list consistent

# set global
regs = []
poll_rate = 1
global regpoll
pollList = []
debugMode = False

class SensorThread(QThread):
    regpoll = pyqtSignal(list)
    def __init__(self):
        QThread.__init__(self)
    def __del__(self):
        self.wait()

    def run(self):
        self.bitsread = 30
        global debugMode
        global regs
        global lenpollList
        c = ModbusClient(host=SERVER_HOST, port=SERVER_PORT)
        while True:
            c.debug(debugMode)
            lenpollList = len(pollList)
            regs_list = ['No Value'] * lenpollList
            if not c.is_open():
                c.open()
            for i in range(0, lenpollList):

                read_in = c.read_input_registers(pollList[i]['address'], pollList[i]['length'])
                print('thing')

                print(pollList[i]['address'])
                if read_in:
                    regs_list[i] = (read_in[0])
                else:
                    regs_list[i] = ('Failed Read')

                regs = regs_list
            self.regpoll.emit(regs)
            time.sleep(poll_rate)


class modbusTool(QtWidgets.QMainWindow, guidesign.Ui_MainWindow):
    disp_enable = True  # Enable for display update

    def __init__(self, parent=None):
        super(modbusTool, self).__init__(parent)
        self.setupUi(self)
        self.createTable()
        self.createTree()
        self.btnStop.setEnabled(False)
        self.btnStart.clicked.connect(self.updateui)
        self.treeWidget.doubleClicked.connect(self.getVarName)
        self.tableWidget.cellDoubleClicked.connect(self.delTableEntry)
        self.checkDebug.stateChanged.connect(self.debugChecked)

    def debugChecked(self, debugState):
        global debugMode
        if debugState:
            debugMode = True
        else:
            debugMode = False


    def createTable(self):
        self.colCount = 2
        self.valColumn = 0
        self.vertDispLimit = 33
        _translate = QtCore.QCoreApplication.translate

        self.tableWidget.setColumnCount(self.colCount)
        if len(pollList) >= self.vertDispLimit:
            self.tableWidget.setRowCount(self.vertDispLimit)
        else:
            self.tableWidget.setRowCount(len(pollList))
        for entries in list(range(0, len(pollList))):
            item = QtWidgets.QTableWidgetItem()
            if entries == self.vertDispLimit:
                self.colCount += 3
                self.valColumn += 3
                self.tableWidget.setColumnCount(self.colCount)
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(self.colCount-3, item)
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(self.colCount-2, item)
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(self.colCount-1, item)
                item = self.tableWidget.horizontalHeaderItem(self.colCount-3)
                item.setText(_translate("MainWindow", "Variable"))
                item = self.tableWidget.horizontalHeaderItem(self.colCount-2)
                item.setText(_translate("MainWindow", "Value"))
                item = self.tableWidget.horizontalHeaderItem(self.colCount-1)
                item.setText(_translate("MainWindow", "Unit"))
            if entries < self.vertDispLimit:
                self.tableWidget.setVerticalHeaderItem(entries, item)
                item = self.tableWidget.verticalHeaderItem(entries)
                item.setText(_translate("MainWindow", pollList[entries]['varname']))
            else:
                self.tableWidget.setItem(entries % self.vertDispLimit, (entries // self.vertDispLimit) * 2, QTableWidgetItem(pollList[entries]['varname']))

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Unit"))
        item.setFlags(QtCore.Qt.ItemIsEnabled)


    def createTree(self):
        _translate = QtCore.QCoreApplication.translate
        self.treeWidget.clear()
        widget = QtWidgets.QTreeWidgetItem(self.treeWidget)
        widget.setText(0, _translate("MainWindow", 'mbrecords'))
        self.fill_item(widget, config_file)
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)


    def fill_item(self, item, value):
        self.last_child = 0
        item.setExpanded(True)
        self.treeWidget.setExpandsOnDoubleClick(True)

        if type(value) is dict:
            for key, val in sorted(value.items()):
                if key == 'mbrecord':
                    return
                child = QTreeWidgetItem()
                self.last_child = child
                child.setText(0, str(key))
                item.addChild(child)
                self.fill_item(child, val)

        '''## Unnecessary section  ##
        elif type(value) is list:
            for val in value:
                child = QTreeWidgetItem()
                self.last_child = child
                item.addChild(child)
                if type(val) is dict:
                    child.setText(0, '[dict]')
                    self.fill_item(child, val)
                elif type(val) is list:
                    child.setText(0, '[list]')
                    self.fill_item(child, val)
                else:
                    child.setText(0, str(val))
                child.setExpanded(True)

        else:
            if not self.last_child:
                child = QTreeWidgetItem()
            else:
                child = self.last_child
            child.setText(0, child.text(0)+ " : " + str(value))
            item.addChild(child)
        ## ##'''

        # Testing
    def delTableEntry(self, row, col):
        print(row, col)
        print(4)
        #


    def updateui(self):
        modbusTool.disp_enable = True
        self.get_thread = SensorThread()
        self.get_thread.start()
        self.get_thread.regpoll.connect(self.handle_trigger)
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(True)
        self.btnStop.clicked.connect(self.pausedisplay)
        self.get_thread.finished.connect(self.done)

    def handle_trigger(self, number):
        if modbusTool.disp_enable:
            for i in list(range(0, len(pollList))):
                self.tableWidget.setItem(i%33, (i//33)*3, QTableWidgetItem(str(number[i])))


    def getVarName(self):
        getSelected = self.treeWidget.currentItem()
        baseNode = getSelected
        if baseNode.childCount() == 0:
            varname_tree = baseNode.text(0)
            getParentNode = baseNode.parent()
            while getParentNode and getParentNode.text(0) != 'mbrecords':
                varname_tree = getParentNode.text(0) + '.' + varname_tree
                getParentNode =  getParentNode.parent()

            for entry in mbmap:
                if varname_tree == entry['varname'] and entry not in pollList:
                    pollList.append(entry)

        self.createTable()

    def pausedisplay(self):
        global debugMode
        modbusTool.disp_enable = False
        self.btnStop.setEnabled(False)
        self.btnStart.setEnabled(True)
        debugMode = False

    def done(self):
        self.btnStop.setEnabled(False)
        self.btnStart.setEnabled(True)

def main():

    global mbmap
    global config_file
    try:
        with open('mbrecords.json') as infile:
            mbmap = json.load(infile)
            infile.close()
    except FileNotFoundError:
        input("mbrecords.json not found. Press enter to continue...")

    with open('config.json') as infile:
        config_file = json.load(infile)
        infile.close()

    app = QtWidgets.QApplication(sys.argv)
    form = modbusTool()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()