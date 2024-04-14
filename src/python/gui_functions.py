
# MAKE THIS INTO A CLASS, RECEIVE THE SERIAL CONFIGURATION AS A PARAMETER FROM THE GUI PRINCIPAL FRAME FILE.

#POSIBLEMENTE SUBIR LOS COMPONENTES A UNA FUNCIÓN Y LLAMARLOS AL INIT Y NO NECESARIAMENTE DESTRUIRLOS, SOLO OCULTAR.


import tkinter as tk
from serial import Serial

class ControlGUI:
    def __init__(self, root: tk.Tk):
        self.serial_conn = Serial(None, 9600, timeout=10)

        self.root = root

        self.main_frame = tk.Frame(self.root)
        self.single_command_frame = tk.Frame(self.root)
        self.multiple_command_frame = tk.Frame(self.root)

        self.components_main_frame()
        self.components_single_commands_frame()
        self.components_multiple_commands_frame()
        
        self.frames = [
            self.main_frame,
            self.single_command_frame,
            self.multiple_command_frame
        ]
        self.main_frame.pack()

    def frame_packer(self, selected_frame):
        for frame in self.frames:
            if frame != selected_frame:
                frame.pack_forget()
                continue
            frame.pack()
            
    def components_main_frame(self):
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
        
        self.single_command_option_button.pack(pady=10)
        self.multiple_commands_window_button.pack(pady=30)

    def components_multiple_commands_frame(self):
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
        
        self.send_button = tk.Button(self.multiple_command_frame, 
                                     text="Send Command", 
                                     command=lambda:send_multiple_commands(self.knob_q1, self.knob_q2, self.knob_q3))

        self.home_button = tk.Button(self.multiple_command_frame, 
                                     text="Return", 
                                     command=lambda:self.frame_packer(self.main_frame))
        
        self.knob_q1.pack(pady=10, padx=10)
        self.knob_q2.pack(pady=20, padx=10)
        self.knob_q3.pack(pady=30, padx=10)
        self.send_button.pack(pady=100)
        self.home_button.pack(pady=10)

    def components_single_commands_frame(self):
        knob = tk.Scale(self.single_command_frame, 
                        from_=0, 
                        to=360, 
                        orient=tk.HORIZONTAL, 
                        label='Knob A')
        
        send_button = tk.Button(self.single_command_frame, 
                                text="Send Command", 
                                command= lambda: print("Sending..."))
        
        home_button = tk.Button(self.single_command_frame, 
                                text="Return", 
                                command=lambda:self.frame_packer(self.main_frame))
        
        knob.pack(pady=10)
        send_button.pack(pady=100)
        home_button.pack(pady=10)














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


