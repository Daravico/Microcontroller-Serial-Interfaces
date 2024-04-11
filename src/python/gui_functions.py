import tkinter as tk

def clear_window(root: tk.Tk):
    for widget in root.winfo_children():
        widget.destroy()

def main_menu_window(root: tk.Tk):
    clear_window(root)

    individual_commands_window_button = tk.Button(root, text="Send Command", command=lambda: individual_commands_window(root))
    individual_commands_window_button.pack()

    group_commands_window_button = tk.Button(root, text="Send Command", command=lambda: group_commands_window(root))
    group_commands_window_button.pack()




def individual_commands_window(root: tk.Tk):
    clear_window(root)

    knob = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label='Knob A')
    knob.pack(pady=10)

    send_button = tk.Button(root, text="Send Command", command= lambda: print("Sending..."))
    send_button.pack(pady=100)

    home_button = tk.Button(root, text="Return", command= lambda: main_menu_window(root))
    home_button.pack(pady=10)

def group_commands_window(root: tk.Tk):
    clear_window(root)

    home_button = tk.Button(root, text="Return", command= lambda: main_menu_window(root))
    home_button.pack(pady=10)


