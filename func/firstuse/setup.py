#!/usr/bin/env python3
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import os
from functools import partial
import getpass

#Set global var username
global username
username = getpass.getuser()

#Create window
window = tk.Tk()

#Set window icon
p1 = PhotoImage(file = f'/home/{username}/pi-ware-pyqt5/icons/logo.png')
window.iconphoto(False, p1)

#Set window title, size, and location
window.title("Setup Pi-Ware")
window.geometry("800x500")
window.eval('tk::PlaceWindow . center')

def StoreData(Data, Location):
    os.system(f"echo '{Data}' > {Location}")
    window.destroy()

#Define labels
heading = tk.Label(window, text="""Setup Pi-Ware""", font="Arial 15 bold")
Thankforinstall = tk.Label(window, text="""Thanks for installing pi-ware!\nLet's set some things up.""", font="Arial 12")
description = tk.Label(window, text="""Do you want Pi-Ware to upload erros, logs and app info to the pi-ware team?\nPlease note, the pi-ware-team can not use this data to:\ntrack, monitor, or be used to identify you.""", font="Arial 12")


#Define buttons
YesButton=tk.Button(window, height=1, width=10, text="Yes", command=lambda: StoreData("True", "$HOME/.local/share/pi-ware-pyqt5/telemetry"))
NoButton=tk.Button(window, height=1, width=10, text="No", command=lambda: StoreData("False", "$HOME/.local/share/pi-ware-pyqt5/telemetry"))

#Pack objects
heading.pack()
Thankforinstall.pack()
description.pack()
YesButton.pack()
NoButton.pack()

window.mainloop()
