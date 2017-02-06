from time import sleep
import threading
from tkinter import *
import tkinter.messagebox
import time
import random
import _thread
import win_inet_pton
import socket
from threading import Thread, Lock
from pyModbusTCP.client import ModbusClient
import json
from pprint import pprint


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 502

# set global
regs = []
poll_rate = 0.5

# init a thread lock
regs_lock = Lock()


class SensorThread(threading.Thread):
    def run(self):
        global regs
        c = ModbusClient(host=SERVER_HOST, port=502)
        while True:
            if not c.is_open():
                c.open()

            reg_list = c.read_input_registers(0)
            if reg_list:
                regs = reg_list[0]
            else:
                regs = 'Connect Error'
            sleep(poll_rate)


class Gui(object):
    ypos = 0


    def __init__(self):
        # create main window
        self.root = tkinter.Tk()
        self.root.title("Modbus Master Tool")
        # Add UI elements
        for entry in mbmap:
            self.dataField(entry['name'])

        self.quitButton()


        self.var = tkinter.StringVar()

        self.ValueLabel = tkinter.Label(self.root, bg='White', textvariable = '7').grid(column=2, row = 1,sticky=E)


    def run(self):

        self.updateGUI()
        self.readSensor()
        self.root.mainloop()

    def updateGUI(self):

        self.root.update()

    def readSensor(self):
        self.var.set = 1
        self.root.update()
        self.root.after(527, self.readSensor)

    # Buttons and such
    def quitButton(self):
        self.quitButton = tkinter.Button(self.root, text='Quit', command=self.root.destroy, height=1, width=3).grid(sticky=S)



    def dataField(self, entry):
        self.GetTempLabel = tkinter.Label(self.root,anchor="w",text=entry).grid(row=Gui.ypos, sticky=W)


        Gui.ypos = Gui.ypos + 1

if __name__ == "__main__":
    global mbmap
    try:
        with open('mbrecords.json') as infile:
            mbmap = json.load(infile)
            infile.close()
    except FileNotFoundError:
        input("mbrecords.json not found. Press enter to continue...")

    pprint(mbmap)

    mbgui = Gui()
    SensorThread().start()
    mbgui.run()