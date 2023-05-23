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

keynames = []
options = []
buttons = []

class MyButton:
    h = 3
    w = 6
    r = 0
    c = 0
    keyname = ""
    def __init__(self, master, c, r, c_sp, r_sp):
        self.button = tkinter.Button(master, height=self.h, width=self.w)#, command=partial(openPopup, master, r, c))
        self.button.bind('<Button-1>', self.set_key)
        self.keyname = keynames[r][c]
        self.button.config(text=keynames[r][c])
        self.button.grid(column=c, row=r, columnspan=c_sp, rowspan=r_sp, padx=2, pady=2)
        self.r = r
        self.c = c
    
    def set_key(self, event):
        self.button["text"] = "Press a Key..."
        self.button.bind('<Key>', self.save_key)
        self.button.focus_set()

    def save_key(self, event):
        key = event.keysym
        self.button.config(text=key)
        saveKey(self.r, self.c, key)
        self.button.unbind('<Key>')
        self.button.unbind('<Button-1>')
        self.button.bind('<Button-1>', self.clear_key)

    def clear_key(self, event):
        self.button["text"] = "Click to Set"
        self.button.unbind('<Button-1>')
        self.button.bind('<Button-1>', self.set_key)

def saveKey(r, c, entry):
    keynames[r][c] = entry
    print(keynames[r][c], entry)
    
    newkeynamesfile = open(os.getcwd()+"\keynames.txt", 'w')
    for h in range(4):
        for j in range(4):
            newkeynamesfile.write(keynames[h][j] + "\n")
            buttons[h][j].button.config(text=keynames[h][j])
    
    newkeynamesfile.close()

'''
# Choose key from list
def openPopup(master, r, c):
    child = tkinter.Toplevel(master)
    child.title("Button config")
    child.geometry("1000x400")

    counter = 0
    col = 0
    row = 0
    for o in range(len(options)):
        newbutton = tkinter.Button(child, text=options[o], width=20, command=partial(saveKey, r, c, options[o]))
        newbutton.grid(column=col, row=row, sticky="W")
        if counter > 17:
            counter = 0
            col = col + 1
        else:
            counter = counter + 1
        if row > 17:
            row = 0
        else:
            row = row + 1
'''

def setup():
    keynamesfile = open(os.getcwd()+"\keynames.txt", 'r')
    optionsfile = open(os.getcwd()+"\options.txt", 'r')

    lines = keynamesfile.readlines()
    k = 0
    for i in range(4):
        temp = []
        for j in range(4):
            if (lines[k].find('\n') != -1): #delete newlines
                temp.append(lines[k][:-1])
            else:
                temp.append(lines[k])
            k = k + 1
        keynames.append(temp)
    
    lines = optionsfile.readlines()
    for line in lines:
        if line.find('\n') != -1:
            options.append(line[:-1])
        else:
            options.append(line)

    keynamesfile.close()
    optionsfile.close()

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
                for h in range(4):
                    j = 3
                    while j >= 0: #iterate in reverse order to get the keys at the right position
                        print(i+k)
                        newfile.write("Keycode."+keynames[j][h] + ", \n")
                        k = k + 1
                        j = j - 1
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
    setup()
    window = tkinter.Tk()
    window.title("Macro Keypad")
    window.geometry('400x400')

    frame1 = tkinter.Frame(window, height=5)
    label1 = tkinter.Label(frame1, text="Macro Keypad Interface", pady=10).pack()
    frame1.pack()

    frame2 = tkinter.Frame(window)
    # Create a 4x4 grid of squares representing the buttons of the keypad
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