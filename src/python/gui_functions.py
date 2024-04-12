
# MAKE THIS INTO A CLASS, RECEIVE THE SERIAL CONFIGURATION AS A PARAMETER FROM THE GUI PRINCIPAL FRAME FILE.

#POSIBLEMENTE SUBIR LOS COMPONENTES A UNA FUNCIÓN Y LLAMARLOS AL INIT Y NO NECESARIAMENTE DESTRUIRLOS, SOLO OCULTAR.


import tkinter as tk
from serial import Serial

class ControlGUI:
    def __init__(self, root: tk.Tk, serial_conn: Serial):
        self.root = root
        self.serial_conn = serial_conn

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def main_menu_frame(self):
        self.clear_window(self.root)

        single_command_option_button = tk.Button(self.root, text="Individual Commands", command=self.single_command_frame)
        single_command_option_button.config(height=2, width=20)
        single_command_option_button.pack(pady=10)

        multiple_commands_window_button = tk.Button(self.root, text="Multiple Commands", command=self.multiple_command_frame)
        multiple_commands_window_button.config(height=2, width=20)
        multiple_commands_window_button.pack(pady=30)

    def multiple_command_frame(self):
        pass

    def single_command_frame(self):
        pass

















def send_single_command():
    pass

def send_multiple_commands(knob_q1: tk.Scale, knob_q2: tk.Scale, knob_q3: tk.Scale):
    Q1_value = knob_q1.get()
    Q2_value = knob_q2.get()
    Q3_value = knob_q3.get()

    command = f'M,Q1-{Q1_value},Q2-{Q2_value},Q3-{Q3_value}'

def clear_window(root: tk.Tk):
    for widget in root.winfo_children():
        widget.destroy()

def main_menu_window(root: tk.Tk):
    clear_window(root)

    single_command_window_button = tk.Button(root, text="Individual Commands", command=lambda: single_command_window(root))
    single_command_window_button.config(height=2, width=20)
    single_command_window_button.pack(pady=10)

    multiple_commands_window_button = tk.Button(root, text="Multiple Commands", command=lambda: multiple_commands_window(root))
    multiple_commands_window_button.config(height=2, width=20)
    multiple_commands_window_button.pack(pady=30)

def single_command_window(root: tk.Tk):
    clear_window(root)

    knob = tk.Scale(root, from_=0, to=360, orient=tk.HORIZONTAL, label='Knob A')
    knob.pack(pady=10)

    send_button = tk.Button(root, text="Send Command", command= lambda: print("Sending..."))
    send_button.pack(pady=100)

    home_button = tk.Button(root, text="Return", command= lambda: main_menu_window(root))
    home_button.pack(pady=10)

def multiple_commands_window(root: tk.Tk):
    clear_window(root)

    knob_q1 = tk.Scale(root, from_=-90, to=90, orient=tk.HORIZONTAL, label='Q1')
    knob_q1.pack(pady=10)

    knob_q2 = tk.Scale(root, from_=0, to=90, orient=tk.HORIZONTAL, label='Q2')
    knob_q2.pack(pady=10)

    knob_q3 = tk.Scale(root, from_=0, to=90, orient=tk.HORIZONTAL, label='Q3')
    knob_q3.pack(pady=10)

    send_button = tk.Button(root, text="Send Command", command= lambda: send_multiple_commands(knob_q1, knob_q2, knob_q3))
    send_button.pack(pady=100)

    home_button = tk.Button(root, text="Return", command= lambda: main_menu_window(root))
    home_button.pack(pady=10)


