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
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 502

# set global
regs = []
poll_rate = 0.5
global resized


class SensorThread(QThread):
    resized = pyqtSignal(list)
    bitsread = 98
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    def run(self):
        global regs
        c = ModbusClient(host=SERVER_HOST, port=SERVER_PORT)
        while True:
            if not c.is_open():
                c.open()
            reg_list = c.read_input_registers(0, SensorThread.bitsread)
            print(reg_list)
            if reg_list:
                regs = reg_list
            else:
                regs = SensorThread.bitsread * ['Failed Read']
            self.resized.emit(regs)


class ExampleApp(QtWidgets.QMainWindow, guidesign.Ui_MainWindow):
    item = []
    last_child = 0
    colCount = 2
    valColumn = 0
    d = {'key1': 'value1',
         'key2': 'value2',
         'key3': [1, 2, 3, {1: 3, 7: 9}],
         'key4': object(),
         'key5': {'another key1': 'another value1',
                  'another key2': 'another value2'}}

    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.createTable()
        self.createTree()
        self.updateui()

    def createTable(self):
        _translate = QtCore.QCoreApplication.translate

        self.tableWidget.setColumnCount(ExampleApp.colCount)
        if len(mbmap) >= 33:
            self.tableWidget.setRowCount(33)
        else:
            self.tableWidget.setRowCount(len(mbmap))
        for i in list(range(0, len(mbmap))):
            item = QtWidgets.QTableWidgetItem()

            if i == 33:
                ExampleApp.colCount += 3
                ExampleApp.valColumn += 3
                self.tableWidget.setColumnCount(ExampleApp.colCount)
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(ExampleApp.colCount-3, item)
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(ExampleApp.colCount-2, item)
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setHorizontalHeaderItem(ExampleApp.colCount-1, item)
                item = self.tableWidget.horizontalHeaderItem(ExampleApp.colCount-3)
                item.setText(_translate("MainWindow", "Variable"))
                item = self.tableWidget.horizontalHeaderItem(ExampleApp.colCount-2)
                item.setText(_translate("MainWindow", "Value"))
                item = self.tableWidget.horizontalHeaderItem(ExampleApp.colCount-1)
                item.setText(_translate("MainWindow", "Unit"))

            if i < 33:
                self.tableWidget.setVerticalHeaderItem(i, item)
                item = self.tableWidget.verticalHeaderItem(i)
                item.setText(_translate("MainWindow", mbmap[i]['name']))
            else:
                self.tableWidget.setItem(i % 33, (i // 33) * 2, QTableWidgetItem(mbmap[i]['name']))

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item.setFlags(QtCore.Qt.ItemIsEnabled)

        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Value"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Unit"))

    def createTree(self):
        _translate = QtCore.QCoreApplication.translate
        self.treeWidget.clear()
        widget = QtWidgets.QTreeWidgetItem(self.treeWidget)
        widget.setText(0, _translate("MainWindow", 'mbrecords'))

        self.fill_item(widget, something)

        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        #self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "List SubMain1"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)

    def fill_item(self, item, value):
        item.setExpanded(True)
        if type(value) is dict:
            for key, val in sorted(value.items()):
                child = QTreeWidgetItem()
                ExampleApp.last_child = child
                child.setText(0, str(key))
                item.addChild(child)
                self.fill_item(child, val)
        elif type(value) is list:
            for val in value:
                child = QTreeWidgetItem()
                ExampleApp.last_child = child
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
            if not ExampleApp.last_child:
                child = QTreeWidgetItem()
            else:
                child = ExampleApp.last_child
            child.setText(0, child.text(0)+ " : " + str(value))
            item.addChild(child)
    def updateui(self):
        self.get_thread = SensorThread()
        self.get_thread.start()
        self.get_thread.resized.connect(self.handle_trigger)
        self.treeWidget.clicked.connect(self.do_something)

    def handle_trigger(self, number):
        for i in list(range(0, len(mbmap))):
            self.tableWidget.setItem(i%33, (i//33)*3, QTableWidgetItem(str(number[i])))
    def do_something(self):
        print("potato")




def main():
    global mbmap
    global something
    try:
        with open('mbrecords_test.json') as infile:
            mbmap = json.load(infile)
            infile.close()
    except FileNotFoundError:
        input("mbrecords.json not found. Press enter to continue...")
    print(len(mbmap))

    with open('config_test.json') as infile:
        something = json.load(infile)
        infile.close()
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()