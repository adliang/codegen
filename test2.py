from time import sleep
import threading
from tkinter import *
import tkinter.messagebox
import time
import random
import _thread

serialdata = []
data = True
x = '5'
class SensorThread(threading.Thread):
    def run(self):
        try:
            i = 0
            while True:
                serialdata.append("%d" % i)
                i += 1
                sleep(0.5)
        except KeyboardInterrupt:
            exit()

class Gui(object):
    def __init__(self):

        self.root = tkinter.Tk()
        self.root.title("Modbus Master Tool")
        self.root.geometry("400x600")
        self.ValueLabel = tkinter.Label(self.root, bg ='White', text="")
        self.updateGUI()
        self.readSensor()
        self.quitButton()
        self.dataField()

    def run(self):
        self.ValueLabel.pack()
        self.ValueLabel.place(x=200, y=80, height=20, width=160)
        self.ValueLabel.after(1000, self.updateGUI)
        self.root.mainloop()

    def updateGUI(self):

        self.root.update()
        self.ValueLabel.after(1000, self.updateGUI)

    def readSensor(self):
        self.ValueLabel["text"] = serialdata[-1]
        self.root.update()
        self.root.after(527, self.readSensor)

    # Buttons and such
    def quitButton(self):
        self.quitButton = tkinter.Button(self.root, text='Quit', command=self.root.destroy, height=1, width=3)
        self.quitButton.pack()
        self.quitButton.place(x=190, y=500)

    def dataField(self):
        self.GetTempLabel = tkinter.Label(self.root,text='Data1 :')
        self.GetTempLabel.pack()
        self.GetTempLabel.place(x=50, y=80, height=20, width=120)

if __name__ == "__main__":
    SensorThread().start()
    Gui().run()