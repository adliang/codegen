import sys
import tkinter

credit = 0
choice = 0

credit1 = 0
coins = 0
prices = [200,150,160,50,90]
item = 0
i = 0
temp=0
n=0
choice1 = 0
choice2 = 0

credit1 = 0
coins = 0
prices = [200,150,160,50,90]
item = 0
i = 0
temp=0
n=0
choice1 = 0
choice2 = 0

def addTENp():
    global credit
    credit+=0.10

def addTWENTYp():
    global credit
    credit+=0.20

def addFIFTYp():
    global credit
    credit+=0.50

def addPOUND():
    global credit
    credit+=1.00

def insert():
    insert = tkinter.Tk()

    insert.geometry("480x360")
    iLabel = tkinter.Label(insert, text="Enter coins.[Press Buttons]").grid(row=1, column=1)

    tenbutton = tkinter.Button(insert, text="10p", command = addTENp).grid(row=2, column=1)
    twentybutton = tkinter.Button(insert, text="20p", command = addTWENTYp).grid(row=3, column=1)
    fiftybutton = tkinter.Button(insert, text="50p", command = addFIFTYp).grid(row=4, column=1)
    poundbutton = tkinter.Button(insert, text="£1", command = addPOUND).grid(row=5, column=1)


insert()