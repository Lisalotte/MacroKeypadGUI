# Macro Keypad GUI
# Author: Lisa Charlotte Pothoven
# 
# A simple GUI to customize the keys on a CircuitPython keypad
#
## TODO:
## Make the array of newkeycodes easily customizable
## Display the current key settings on the grid
## Add RGB options
#

import tkinter
import numpy as np
from functools import partial
from tkinter import filedialog
import os

newkeycodes = [
    "Keycode.A,",
    "Keycode.A,",
    "Keycode.A,",
    "Keycode.A,",
    "Keycode.B,",
    "Keycode.B,",
    "Keycode.B,",
    "Keycode.B,",
    "Keycode.C,",
    "Keycode.C,",
    "Keycode.C,",
    "Keycode.C,",
    "Keycode.D,",
    "Keycode.D,",
    "Keycode.D,",
    "Keycode.D"
]
keynames = [["A", "A", "A", "A"],
            ["A", "A", "A", "A"],
            ["A", "A", "A", "A"],
            ["B", "E", "I", "Z"]]

class MyButton:
    h = 3
    w = 6
    keyname = ""
    def __init__(self, master, c, r, c_sp, r_sp):
        self.button = tkinter.Button(master, height=self.h, width=self.w)
        self.keyname = keynames[r][c]
        self.button.config(text=keynames[r][c])
        self.button.grid(column=c, row=r, columnspan=c_sp, rowspan=r_sp, padx=2, pady=2)

def askDir(codepath, mystring):
    '''
    dir = filedialog.askdirectory()
    codepath.delete(0,'end')
    codepath.insert(0, dir)
    '''    
    code = filedialog.askopenfile()
    codepath.delete(0,'end')
    codepath.insert(0, code.name)
    mystring.set(code.name)

def findInCode(keyword, mystring):
    filepath = mystring.get()
    file = open(filepath, 'r')    
    newfile = open(filepath[:-7]+"newcode.py", 'w')    

    lines = file.readlines()
    line_nr = 0
    k = 0
    for i in range(len(lines)):
        i=i+k      
        if (i < len(lines)):
            if (lines[i].find(keyword) != -1):
                line_nr = lines.index(lines[i])         
                newfile.write(lines[i])
                print(i)
                k = k + 1
                newfile.write(lines[i + k])
                for j in range(len(newkeycodes)):
                    print(i+k)
                    newfile.write(newkeycodes[j] + "\n")
                    k = k + 1
                #newfile.write("] \n")
                #i=i+1            
            else:
                print("else:", i)
                newfile.write(lines[i])

    file.close()
    newfile.close()
    os.rename(filepath, filepath[:-3]+"_old.py")
    os.rename(filepath[:-7]+"newcode.py", filepath)

def main():
    window = tkinter.Tk()
    window.title("Macro Keypad")
    window.geometry('400x400')

    frame1 = tkinter.Frame(window, height=5)
    label1 = tkinter.Label(frame1, text="Macro Keypad Interface", pady=10).pack()
    frame1.pack()

    frame2 = tkinter.Frame(window)
    # Create a 4x4 grid of squares representing the buttons of the keypad
    buttons = []
    for i in range(4):
        newrow = []
        for j in range (4):
            btn = MyButton(frame2,j,i,1,1)
            newrow.append(btn)
        buttons.append(newrow)    

    frame2.pack()

    frame3 = tkinter.Frame(window, pady=10)

    mystring = tkinter.StringVar(frame3, value="C:/Users/Lisa/Documents/Raspberry Pi/Pico/code.py")
    codepath = tkinter.Entry(frame3, textvariable=mystring, width=60)
    codepath_btn = tkinter.Button(frame3, text="Locate Keypad", command=partial(askDir,codepath, mystring))
    
    codepath.grid(column=0,row=1, sticky="N")
    codepath_btn.grid(column=0,row=0, pady=10, sticky="S")

    find_btn = tkinter.Button(frame3, text="Find keyword", command=partial(findInCode, "targetkeymap", mystring))
    find_btn.grid(column=0,row=2)

    frame3.pack()

    window.mainloop()

if __name__ == "__main__":
	main()