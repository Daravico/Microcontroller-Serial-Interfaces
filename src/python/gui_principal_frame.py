import tkinter as tk
import gui_functions

root = tk.Tk()
root.title("Robot Serial Interface")
root.geometry('400x600')

control_gui = gui_functions.ControlGUI(root)

root.mainloop()