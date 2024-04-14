import tkinter as tk
import gui_functions

root = tk.Tk()
root.title("Robot Serial Interface")
root.geometry('100x100')

#frame = tk.Frame(root, padx=100, pady=100)
#frame.pack(padx=100, pady=100)

control_gui = gui_functions.ControlGUI(root)

#gui_functions.main_menu_window(frame)

root.mainloop()