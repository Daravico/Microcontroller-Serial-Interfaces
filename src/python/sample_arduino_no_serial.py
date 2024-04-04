import tkinter as tk
from pyfirmata import Arduino

# ------------
# DESCRIPTION:
# This sample code is to test the library of Arduino from pyfirmata.
# No code for serial connection with a valid functionality has been developed.
# ------------

'''
Does not require the serial library
'''

# ------------------------------------------------------------------------

# Serial port to be connected. 
board = Arduino("COM3")

def ledOn():
    board.digital[13].write(1)
def ledOff():
    board.digital[13].write(0)

# Root widget to create window
win = tk.Tk()
# initialize window with title & minimum size
win.title("L E D")
win.minsize(200,60)

# Label widget
label = tk.Label(win, text="click to turn ON/OFF")
label.grid(column=1, row=1)

# Button widget
ONbtn = tk.Button(win, bd=4, text="LED ON", command=ledOn)
ONbtn.grid(column=1, row=2)
OFFbtn = tk.Button(win, bd=4, text="LED OFF", command=ledOff)
OFFbtn.grid(column=2, row=2)

# start & open window continously
win.mainloop()