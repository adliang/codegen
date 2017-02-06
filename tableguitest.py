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

            reg_list = c.read_input_registers(0,8)
            if reg_list:
                regs = reg_list
            else:
                regs = 'Connect Error'
            sleep(poll_rate)


class Gui(object):
    ypos = 0
    label = {}


    def __init__(self):
        # create main window
        self.root = tkinter.Tk()
        self.root.title("Modbus Master Tool")
        self.root.geometry("400x600")

        # Add UI elements
        for entry in mbmap:
            Gui.lb = Label(self.root, bg='White', text="")
            Gui.lb.grid(column=2, row=Gui.ypos, sticky=E)
            Gui.label[Gui.ypos] = Gui.lb
            self.dataField(entry['name'])
        self.quitButton()
        self.var = tkinter.StringVar()


    def run(self):
        for i in (range(len(Gui.label)-1)):
            Gui.label[i].after(500, lambda:self.updateGUI)
        self.updateGUI()
        self.readSensor()
        self.root.mainloop()

    def updateGUI(self):

        self.root.update()

        for i in (range(len(Gui.label)-1)):
            Gui.label[i].after(500, lambda:self.updateGUI)

    def readSensor(self):
        for i in (range(len(Gui.label))):
            if regs:
                Gui.label[i]["text"] = regs[i]
            else:
                Gui.label[i]["text"] = "Connect Error"
        #self.var.set = 1
        self.root.update()
        self.root.after(500, self.readSensor)

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
    except:
        input("mbrecords.json not found. Press enter to continue...")

    pprint(mbmap)

    mbgui = Gui()


    SensorThread().start()
    mbgui.run()