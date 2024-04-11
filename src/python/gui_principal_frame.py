import tkinter as tk
import gui_functions



root = tk.Tk()
root.title("Robot Serial Interface")

frame = tk.Frame(root)
frame.pack(padx=100, pady=100)

'''



other_button = tk.Button(frame, text="load", command= lambda: gui_functions.individual_commands_window(frame))
other_button.pack(pady=20)
'''

gui_functions.main_menu_window(frame)

root.mainloop()