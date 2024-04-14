

# Realizar modificaciones para añadir un botón que establezca la configuración de SERIAL con el archivo creado de 
# serial_configuration

import tkinter as tk
from tkinter import ttk
from serial import Serial
import serial_configuration

class ControlGUI:
    # oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo
    def __init__(self, root: tk.Tk):
        self.serial_conn = Serial(None, 9600, timeout=10)

        self.root = root

        self.main_frame = tk.Frame(self.root)
        self.single_command_frame = tk.Frame(self.root)
        self.multiple_command_frame = tk.Frame(self.root)

        # ______________

        self.serial_configuration_button = tk.Button(self.main_frame,
                                                     text="Serial Configuration",
                                                     command=self.get_ports,
                                                     height=2,
                                                     width=20)

        self.single_command_option_button = tk.Button(self.main_frame, 
                                                 text="Individual Commands", 
                                                 command=lambda:self.frame_packer(self.single_command_frame), 
                                                 height=2,
                                                 width=20)
        
        self.multiple_commands_window_button = tk.Button(self.main_frame, 
                                                    text="Multiple Commands", 
                                                    command=lambda:self.frame_packer(self.multiple_command_frame),
                                                    height=2, 
                                                    width=20)
        
        # ______________

        self.combo_serial = ttk.Combobox(self.single_command_frame,
                                  values=serial_configuration.show_ports())
        
        # ______________

        self.knob = tk.Scale(self.single_command_frame, 
                        from_=0, 
                        to=360, 
                        orient=tk.HORIZONTAL, 
                        label='Knob A')
        
        self.combo_joint = ttk.Combobox(self.single_command_frame,
                                  values=['Q1', 'Q2', 'Q3'])
        
        self.combo_joint.set("Q1")
        
        self.send_single_button = tk.Button(self.single_command_frame, 
                                text="Send Command", 
                                command=self.send_single_command)
        
        self.home_single_button = tk.Button(self.single_command_frame, 
                                text="Return", 
                                command=lambda:self.frame_packer(self.main_frame))

        # ______________

        self.knob_q1 = tk.Scale(self.multiple_command_frame, 
                                from_=-90, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                label='Q1')
        
        self.knob_q2 = tk.Scale(self.multiple_command_frame, 
                                from_=0, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                label='Q2')
        
        self.knob_q3 = tk.Scale(self.multiple_command_frame, 
                                from_=0, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                label='Q3')
        
        self.send_multiple_button = tk.Button(self.multiple_command_frame, 
                                     text="Send Command", 
                                     command=self.send_multiple_commands)

        self.home_multiple_button = tk.Button(self.multiple_command_frame, 
                                     text="Return", 
                                     command=lambda:self.frame_packer(self.main_frame))
        
        # ______________

        self.serial_configuration_button.pack(pady=10)
        self.single_command_option_button.pack(pady=40)
        self.multiple_commands_window_button.pack(pady=50)
        
        self.knob.pack(pady=10)
        self.combo_joint.pack(pady=10)
        self.send_single_button.pack(pady=50)
        self.home_single_button.pack(pady=100)

        self.knob_q1.pack(pady=10, padx=10)
        self.knob_q2.pack(pady=20, padx=10)
        self.knob_q3.pack(pady=30, padx=10)
        self.send_multiple_button.pack(pady=100)
        self.home_multiple_button.pack(pady=10)

        # ______________

        self.frames = [
            self.main_frame,
            self.single_command_frame,
            self.multiple_command_frame
        ]

        self.main_frame.pack()

    # oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo

    def get_ports(self):
        for port in sorted(serial_configuration.show_ports()):
                print(f"{port}: {port.device}")
        
        

    # ------------------------------------------------------------------------

    def frame_packer(self, selected_frame):
        for frame in self.frames:
            if frame != selected_frame:
                frame.pack_forget()
                continue
            frame.pack()
            
    # ------------------------------------------------------------------------

    def send_single_command(self):
        Q_value = self.knob.get()
        selected_Q = self.combo_joint.get()

        command = f'S#{selected_Q}-{Q_value}'

        print(command)

    # ------------------------------------------------------------------------

    def send_multiple_commands(self):
        Q1_value = self.knob_q1.get()
        Q2_value = self.knob_q2.get()
        Q3_value = self.knob_q3.get()

        command = f'M#Q1-{Q1_value},Q2-{Q2_value},Q3-{Q3_value}'

        print(command)

    # oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo



'''
# OBSOLETE.


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

'''
