import tkinter as tk
from tkinter import ttk
from typing import List
from principal_window import FrameHandler

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class MainMenuFrame(tk.Frame):
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):

        # Calling the original constructor to keep the properties.
        tk.Frame.__init__(self, root)

        self.root = root

        self.name = 'main_frame'

        self.serial_configuration_button = tk.Button(self,
                                                     text="Serial Configuration",
                                                     command=lambda: frame_handler.frame_packer('serial_frame'),
                                                     height=2,
                                                     width=20)
        
        self.direct_kinematics_frame_button = tk.Button(self, 
                                                        text="Direct Kinematics", 
                                                        command=None,
                                                        height=2, 
                                                        width=20)
        
        self.inverse_kinematics_frame_button = tk.Button(self, 
                                                        text="Inverse Kinematics", 
                                                        command=None,
                                                        height=2, 
                                                        width=20)
        
        self.exit_window_button = tk.Button(self, 
                                            text="Exit", 
                                            command=self.root.destroy,
                                            height=2, 
                                            width=20)

        # Main frame components placing.
        self.serial_configuration_button.place(relx=0.5, rely=0.3, anchor='center')
        self.direct_kinematics_frame_button.place(relx=0.5, rely=0.4, anchor='center')
        self.inverse_kinematics_frame_button.place(relx=0.5, rely=0.5, anchor='center')
        self.exit_window_button.place(relx=0.5, rely=0.7, anchor='center')


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class SerialConfigurationFrame(tk.Frame):
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        # Calling the original constructor to keep the properties.
        tk.Frame.__init__(self, root)

        self.root = root

        self.name = 'serial_frame'

        self.load_serial_button = tk.Button(self, 
                                            text="Load Ports", 
                                            command=None,
                                            height=2, 
                                            width=20)

        self.combo_serial = ttk.Combobox(self)
        
        # TODO: IMPORT FUNCTION.
        self.combo_serial.bind('<<ComboboxSelected>>', None)

        self.selected_port_name_label = tk.Label(self,
                                                 text="NONE")
        
        self.selected_port_desc_label = tk.Label(self,
                                                text="...")
        
        # TODO: Add correct validations.
        self.baudrate_entry = tk.Entry(self, 
                                    textvariable=None,#self.serial_baudrate_value,
                                    validate="key",
                                    validatecommand=(self.root.register(None), "%P"))
        
        self.update_serial_configuration_button = tk.Button(self,
                                                            text="Update",
                                                            command=None)
        
        self.home_serial_configuration_button = tk.Button(self, 
                                                        text="Return", 
                                                        command=lambda: frame_handler.frame_packer('main_frame'))

        # Serial Configuration frame components packing.
        self.load_serial_button.place(relx=0.5, rely=0.2, anchor='center')
        self.selected_port_name_label.place(relx=0.5, rely=0.3, anchor='center')
        self.selected_port_desc_label.place(relx=0.5, rely=0.4, anchor='center')
        self.combo_serial.place(relx=0.5, rely=0.5, anchor='center')
        self.baudrate_entry.place(relx=0.5, rely=0.6, anchor='center')
        self.update_serial_configuration_button.place(relx=0.5, rely=0.7, anchor='center')
        self.home_serial_configuration_button.place(relx=0.5, rely=0.8, anchor='center')

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class RoboticConfigurationFrame(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class DirectKinematicsFrame(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class InverseKinematicsFrame(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
