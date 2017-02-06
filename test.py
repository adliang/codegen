import tkinter
import tkinter.messagebox
import time
import random
import _thread

class Menu:

    def __init__(self):
        #Frames
        self.frame_2 = tkinter.Frame(self.main_window, bg='white') # Receiving DATAs

        #ReceiveLabel
        self.ReceiveLabel = tkinter.Label(self.frame_2,\
                                       text = 'Received DATAs',\
                                       bg = 'White',\
                                       height = 2, width = 20)

        #Temperature
        self.GetTempLabel = tkinter.Label(self.frame_2,\
                                       text='Temperature :')
        self.TempValue = tkinter.StringVar()

        self.GetTempValueLabel = tkinter.Label(self.frame_2,bg = 'White',\
                                               textvariable = self.TempValue
                                               )

        #PACKING
        self.frame_2.pack()
        self.frame_2.place(x=410, y=0, height=300, width=400)
        #ReceiveLabel
        self.ReceiveLabel.pack()
        self.ReceiveLabel.place(x=100, y=10)
        #Temperature
        self.GetTempLabel.pack()
        self.GetTempLabel.place(x=50, y=80, height=20, width=120)
        self.GetTempValueLabel.pack()
        self.GetTempValueLabel.place(x=200, y=80, height=20, width=160)




        self.main_window.after(2000, _thread.start_new_thread, self.GetTemp, ())
        tkinter.mainloop()

    def GetTemp(self):

        while(1):
            value = random.random()
            self.TempValue.set(str(value))
            time.sleep(0.5)

gui = Menu()