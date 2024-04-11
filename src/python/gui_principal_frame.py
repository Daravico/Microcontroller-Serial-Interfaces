import tkinter as tk
import gui_functions

root = tk.Tk()
root.title("Robot Serial Interface")

frame = tk.Frame(root)
frame.pack(padx=100, pady=100)

gui_functions.main_menu_window(frame)

root.mainloop()