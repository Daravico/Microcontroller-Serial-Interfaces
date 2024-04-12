import tkinter as tk
import gui_functions
import serial

serial_conn = serial.Serial('COM4', 9600, timeout=10)

root = tk.Tk()
root.title("Robot Serial Interface")

frame = tk.Frame(root)
frame.pack(padx=100, pady=100)

control_gui = gui_functions.ControlGUI(frame, serial_conn)



#gui_functions.main_menu_window(frame)

root.mainloop()