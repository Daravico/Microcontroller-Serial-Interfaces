import tkinter as tk
from tkinter import ttk
from typing import List
from serial_library import SerialObject

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class FrameHandler:
    def __init__(self):
        self.frames:List[GeneralFrame] = [] 

    # ------------------------------------------------

    def frame_packer(self, frame_name:str):
        '''
        Function used to update the frame that is being selected.
        :selected_frame: is searched in the list of the available frames in order to be loaded. Any other frame is forgoten from the root.
        '''
        for frame in self.frames:
            if frame.name != frame_name:
                frame.pack_forget()
                continue
            frame.pack(expand=True, fill='both')

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class GeneralFrame(tk.Frame):
    '''

    '''
    def __init__(self, root:tk.Tk, name: str, frame_handler:FrameHandler):
        tk.Frame.__init__(self, root)
        self.frame_handler=frame_handler 
        self.root = root
        self.name = name

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class MainMenuFrame(GeneralFrame):
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        GeneralFrame.__init__(self, root, 'main_frame', frame_handler)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.serial_configuration_button = tk.Button(self,
                                                     text="Serial Configuration",
                                                     command=lambda: frame_handler.frame_packer('serial_configuration_frame'),
                                                     height=2,
                                                     width=20)
        
        # TODO: Add functionalities.
        self.robotic_configuration_button = tk.Button(self,
                                                      text="Robotic Configuration",
                                                      command=None,#lambda: frame_handler.frame_packer('robotic_configuration_frame'),
                                                      height=2,
                                                      width=20)

        self.direct_kinematics_frame_button = tk.Button(self, 
                                                        text="Direct Kinematics", 
                                                        command=lambda: frame_handler.frame_packer('direct_kinematics_frame'),
                                                        height=2, 
                                                        width=20)
        
        # TODO: Add functionalities.
        self.inverse_kinematics_frame_button = tk.Button(self, 
                                                        text="Inverse Kinematics", 
                                                        command=None,#lambda: frame_handler.frame_packer('inverse_kinematics_frame'),
                                                        height=2, 
                                                        width=20)
        
        self.exit_window_button = tk.Button(self, 
                                            text="Exit", 
                                            command=self.root.destroy,
                                            height=2, 
                                            width=20)

        # Main frame components placing.
        self.serial_configuration_button.place(relx=0.5, rely=0.3, anchor='center')
        self.robotic_configuration_button.place(relx=0.5, rely=0.4, anchor='center')
        self.direct_kinematics_frame_button.place(relx=0.5, rely=0.5, anchor='center')
        self.inverse_kinematics_frame_button.place(relx=0.5, rely=0.6, anchor='center')
        self.exit_window_button.place(relx=0.5, rely=0.8, anchor='center')


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class SerialConfigurationFrame(GeneralFrame):
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler, serial_conn:SerialObject):
        GeneralFrame.__init__(self, root, 'serial_configuration_frame', frame_handler)

        # Serial object reference.
        self.serial_conn = serial_conn

        # Port data.
        self.available_ports_data = {}

        # Baudrate values reference.
        self.serial_baudrate_value = tk.StringVar(self.root)
        self.serial_baudrate_value.set(self.serial_conn.baudrate)
        
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.load_serial_button = tk.Button(self, 
                                            text="Load Ports", 
                                            command=self.load_ports,
                                            height=2, 
                                            width=20)

        self.combo_serial = ttk.Combobox(self)
        
        self.combo_serial.bind('<<ComboboxSelected>>', self.update_label_serial_port)

        self.selected_port_name_label = tk.Label(self,
                                                 text="NONE")
        
        self.selected_port_desc_label = tk.Label(self,
                                                text="...")
        
        # TODO: Add correct validations. Add the starting value.
        self.baudrate_entry = tk.Entry(self, 
                                    textvariable=self.serial_baudrate_value,
                                    validate="key",
                                    validatecommand=(self.root.register(self.baudrate_entry_number_validation), "%P"))
        
        self.update_serial_configuration_button = tk.Button(self,
                                                            text="Update",
                                                            command=self.update_serial_configuration)
        
        self.home_serial_configuration_button = tk.Button(self, 
                                                        text="Return", 
                                                        command=lambda: frame_handler.frame_packer('main_frame'),
                                                        height=2, 
                                                        width=20)

        # Serial Configuration frame components packing.
        self.load_serial_button.place(relx=0.5, rely=0.2, anchor='center')
        self.selected_port_name_label.place(relx=0.5, rely=0.3, anchor='center')
        self.selected_port_desc_label.place(relx=0.5, rely=0.4, anchor='center')
        self.combo_serial.place(relx=0.5, rely=0.5, anchor='center')
        self.baudrate_entry.place(relx=0.5, rely=0.6, anchor='center')
        self.update_serial_configuration_button.place(relx=0.5, rely=0.7, anchor='center')
        self.home_serial_configuration_button.place(relx=0.5, rely=0.8, anchor='center')

        # Loading the available ports.
        self.load_ports()

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # - - - - - - - - - - Methods - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def load_ports(self):
        '''
        The function is used by a button who loads and refresh the
        current available port list in order for these to be selected
        in the combobox (combo_serial).
        '''
        ports_data = self.serial_conn.get_ports()
        
        self.available_ports_data = {}

        for port, description, _ in ports_data:
            self.available_ports_data[port] = description
        
        listed_ports = list(self.available_ports_data.keys())

        self.combo_serial.configure(values=listed_ports)

    # ------------------------------------------------

    def update_label_serial_port(self, _):
        '''
        This function updates the labels destinated to display the current selection
        for the serial configuration in regards to the port information exclusively.
        '''
        # Extracting the information.
        selected_port = self.combo_serial.get()
        description = self.available_ports_data[selected_port]

        # Labels update.
        self.selected_port_name_label.configure(text=selected_port)
        self.selected_port_desc_label.configure(text=description)

    # ------------------------------------------------

    def baudrate_entry_number_validation(self, new_value:str):
        '''
        Callback function that is called when a new entry is set for the baudrate.
        This confirms if it is a number or a blank space in order to avoid chars in
        the value required as int.
        '''
        if new_value.isdigit() or new_value == "":
            return True
        return False
    
    # ------------------------------------------------

    def update_serial_configuration(self):
        '''
        Casting the value of the variable holding the baudrate from the entry
        to an integer and updating the configuration for the serial port.
        '''
        # No baudrate specified.
        if self.baudrate_entry.get() == '':
            return
        # No port selected.
        if self.combo_serial.get() == None or self.combo_serial.get() == "":
            print("No changes")
            return
        
        self.serial_conn.port = self.combo_serial.get()
        self.serial_conn.baudrate = int(self.serial_baudrate_value.get())
        
        # TODO: Remove.
        print(f'PORT: {self.serial_conn.port} | BAUDRATE: {self.serial_conn.baudrate}')


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class RoboticConfigurationFrame(GeneralFrame):
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        GeneralFrame.__init__(self, root, 'robotic_configuration_frame', frame_handler)

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class DirectKinematicsFrame(GeneralFrame):
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        GeneralFrame.__init__(self, root, 'direct_kinematics_frame', frame_handler)

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class InverseKinematicsFrame(GeneralFrame):
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        GeneralFrame.__init__(self, root, 'inverse_kinematics_frame', frame_handler)
