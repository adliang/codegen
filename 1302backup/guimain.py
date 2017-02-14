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
from PyQt5.QtCore import QThread, pyqtSignal, QObject, QTimer
from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QTreeView, QTableWidget, QTableWidgetItem, QSpinBox
import logging
import struct

x=0
servers = ["127.0.0.1", "192.168.1.71"]

SERVER_HOST = servers[x]
SERVER_PORT = 502

# set global
global regpoll
pollList = []
regs = []


class SensorThread(QThread):
    regpoll = pyqtSignal(list)
    poll_rate = 1
    c = ModbusClient(host=SERVER_HOST, port=SERVER_PORT, auto_open=True, auto_close=True)
    global pollEn
    pollEn = True

    def __init__(self):
        QThread.__init__(self)


    def __del__(self):
        self.wait()


    def writeToReg(self, writeArray, addrArray):

        print(writeArray)
        print(addrArray)
        for i in range(len(writeArray)):
          if writeArray[i]:
              self.c.write_multiple_registers(addrArray[i], writeArray[i])


    def debugToggle(self, state):
        self.c.debug(state)


    def setPollRate(self, pollRate):
        SensorThread.poll_rate = pollRate
        print(SensorThread.poll_rate)


    def run(self):
        global regs
        global lenpollList

        if SensorThread.pollEn:
            while True:
                if pollList:
                    regs_list = ['No Value Read'] * lenpollList

                    for i in range(0, lenpollList):
                        try:
                            read_in = self.c.read_holding_registers(pollList[i]['address'], pollList[i]['length'])

                            if read_in:
                                regs_list[i] = (read_in)

                        except IndexError:
                            print('error')
                            pass
                    regs = regs_list
                    print(regs)
                    print("------------------------------------------------------")
                    self.regpoll.emit(regs)
                time.sleep(SensorThread.poll_rate)


class modbusTool(QtWidgets.QMainWindow, guidesign.Ui_MainWindow):

    disp_enable = True  # Enable for display update

    colValue = 0
    colUnit = 1
    colWrite = 2
    colRemove = 3
    colMsg = 4

    endianABCD = 0  # Big Endian Bytes, Reg 1 MSW
    endianCDAB = 1  # Big Endian Bytes, Reg 2 MSW

    endian = endianABCD # Endian for floats

    def __init__(self, parent=None):
        super(modbusTool, self).__init__(parent)
        self.setupUi(self)
        self.createTree()
        self.updateTable()
        self.updateWriteButton()
        self.setPollRate()
        self.btnStop.setEnabled(False)
        self.btnStart.clicked.connect(self.updateui)
        self.treeWidget.doubleClicked.connect(self.addTableEntry)
        self.tableWidget.cellDoubleClicked.connect(self.delTableEntry)
        self.checkDebug.stateChanged.connect(self.debugModeToggle)
        self.btnWrite.clicked.connect(self.writeToReg)
        self.spinBoxPollRate.valueChanged.connect(self.setPollRate)
        self.comboBoxDataEncode.currentIndexChanged.connect(self.set_endian)


    # ---------------------------------------------------------------------------#
    # Creating tree widget from config.json
    # ---------------------------------------------------------------------------#
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
        item.setExpanded(False)
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


    # ---------------------------------------------------------------------------#
    # Starts polling on start clicked
    # ---------------------------------------------------------------------------#
    def updateui(self):
        SensorThread.pollEn = True
        self.debugModeToggle()
        modbusTool.disp_enable = True
        self.get_thread = SensorThread()
        self.get_thread.start()
        self.get_thread.regpoll.connect(self.updateValues)
        self.btnStart.setEnabled(False)
        self.btnStop.setEnabled(True)
        self.btnStop.clicked.connect(self.pausedisplay)
        self.get_thread.finished.connect(self.done)


    # ---------------------------------------------------------------------------#
    # Stop button action
    # ---------------------------------------------------------------------------#
    def pausedisplay(self):

        #modbusTool.disp_enable = False
        SensorThread.pollEn = False
        self.btnStop.setEnabled(False)
        self.btnStart.setEnabled(True)
        SensorThread().debugToggle(False)


    # ---------------------------------------------------------------------------#
    # Connects debug checkbox to debug mode toggle
    # ---------------------------------------------------------------------------#
    def debugModeToggle(self):
        if self.checkDebug.checkState():
            SensorThread().debugToggle(True)
        else:
            SensorThread().debugToggle(False)


    # ---------------------------------------------------------------------------#
    # Write to register
    # ---------------------------------------------------------------------------#
    def updateWriteButton(self):
        if pollList:
            self.btnWrite.setEnabled(True)
        else:
            self.btnWrite.setEnabled(False)


    def writeToReg(self):
        global lenpollList
        valToWrite = []
        addrToWrite = []
        U32 = 2
        F32 = 2
        INT = 1
        D64 = 4
        uShort = 'H'

        self.btnWrite.setEnabled(False)
        for row in list(range(0, lenpollList)):
            writeValue = self.tableWidget.item(row, modbusTool.colWrite)

            if writeValue:
                try:
                    if pollList[row]['type'] == 'int':
                        foo = struct.pack('>H', int(writeValue.text()))
                        pack_id = '>' + INT * uShort
                    if pollList[row]['type'] == 'U32':
                        foo = struct.pack('>L', int(writeValue.text()))
                        pack_id = '>' + U32 * uShort
                    if pollList[row]['type'] == 'F32':
                        foo = struct.pack('>f', int(writeValue.text()))
                        pack_id = '>' + F32 * uShort
                    if pollList[row]['type'] == 'D64':
                        foo = struct.pack('>d', int(writeValue.text()))
                        pack_id = '>' + D64 * uShort
                    fi = struct.unpack(pack_id, foo)
                    if modbusTool.endian == modbusTool.endianCDAB:
                        reversedFi = [i for i in reversed(fi)]
                        fi=reversedFi
                    valToWrite.append(fi)

                    self.tableWidget.setItem(row, modbusTool.colMsg, QTableWidgetItem('Write Success %s' % writeValue.text()))
                    self.tableWidget.setItem(row, modbusTool.colWrite, QTableWidgetItem(None))
                except ValueError:
                    self.tableWidget.setItem(row, modbusTool.colMsg, QTableWidgetItem('Invalid Data'))
                    continue
            else:
                valToWrite.append(None)
            addrToWrite.append(pollList[row]['address'])
        SensorThread().writeToReg(valToWrite, addrToWrite)
        self.btnWrite.setEnabled(True)


    # ---------------------------------------------------------------------------#
    # Updates table value field on modbus polling
    # ---------------------------------------------------------------------------#
    def set_endian(self, endianVal):
            modbusTool.endian = endianVal


    def setPollRate(self):
        SensorThread.poll_rate = self.spinBoxPollRate.value()


    def updateValues(self, poll_value):
        # Struct arguments
        uShort = 'H'
        uInt16 = 'I'
        uLong32 = 'L'
        float32 = 'f'
        double64 = 'd'
        little_end = '<'
        big_end = '>'

        # Config type identifiers
        U32 = 'U32'
        F32 = 'F32'
        INT = 'int'
        D64 = 'D64'

        if modbusTool.disp_enable:

            for i in list(range(0, len(pollList))):
                try:
                    if poll_value[i] == 'No Value Read':
                        self.tableWidget.setItem(i, 0, QTableWidgetItem(str(poll_value[i])))
                    else:
                        pack_id = big_end + len(poll_value[i]) * uShort
                        if modbusTool.endian == modbusTool.endianCDAB:
                            poll_value[i].reverse()
                        foo = struct.pack(pack_id, *poll_value[i])

                        try:

                            if pollList[i]['type'] == U32:
                                fi = struct.unpack(big_end+uLong32, foo)
                            elif pollList[i]['type'] == F32:
                                fi = struct.unpack(big_end+float32, foo)
                            elif pollList[i]['type'] == INT:
                                fi = struct.unpack(big_end+uShort, foo)
                            elif pollList[i]['type'] == D64:
                                fi = struct.unpack(big_end + double64, foo)
                            self.tableWidget.setItem(i, modbusTool.colValue, QTableWidgetItem(str(fi[0])))
                        except struct.error:
                            self.tableWidget.setItem(i, modbusTool.colMsg, QTableWidgetItem(str('Invalid Type/Length Match')))

                # If poll list has changed during value update, will result in error
                except IndexError:
                    pass
        self.tableWidget.resizeColumnsToContents()


    # ---------------------------------------------------------------------------#
    # Table entries updating
    # ---------------------------------------------------------------------------#
    def updateTable(self):
        _translate = QtCore.QCoreApplication.translate
        self.tableWidget.setRowCount(len(pollList))

        for entries in list(range(0, len(pollList))):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setVerticalHeaderItem(entries, item)
            item = self.tableWidget.verticalHeaderItem(entries)
            item.setText(_translate("MainWindow", pollList[entries]['varname']))
            item = QtWidgets.QTableWidgetItem()
            item.setFlags(QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(0, modbusTool.colRemove, item)
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.resizeColumnsToContents()
        self.updateWriteButton()


    def delTableEntry(self, row, col):
        global lenpollList
        if col == modbusTool.colRemove:
            pollList.remove(pollList[row])
            self.updateTable()
            lenpollList = len(pollList)
            self.updateWriteButton()


    def addTableEntry(self):
        global lenpollList
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
        lenpollList = len(pollList)
        self.updateTable()


    # ---------------------------------------------------------------------------#
    # Thread finished action
    # ---------------------------------------------------------------------------#
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
