
import tkinter as tk
from tkinter import ttk
from tkdial import Dial
from serial import Serial
import serial_configuration


'''
Class with all the implementations for the current GUI design and methods used to communicate the controller
with the robot. No specific Micro is required, it is only needed the considerations in the codes being sent 
through the serial communication. The instance also establishes the configuration for the serial communication.
'''

class ControlGUI:

    def __init__(self, root: tk.Tk):
        # Serial variables and configuration.
        self.serial_conn = Serial(None, 9600, timeout=10)
        self.available_ports_data = {}

        # Root object for tkinter passed as a parameter.
        self.root = root

        # Frames created and used for the robot controller.
        self.main_frame = tk.Frame(self.root)
        self.serial_configuration_frame = tk.Frame(self.root)
        self.single_command_frame = tk.Frame(self.root)
        self.multiple_command_frame = tk.Frame(self.root)

        # ----------------------------------
        # SECTION: COMPONENTS INITIALIZATION.
        # ----------------------------------

        # @ @ @ Main Frame components @ @ @

        self.serial_configuration_button = tk.Button(self.main_frame,
                                                     text="Serial Configuration",
                                                     command=lambda:self.frame_packer(self.serial_configuration_frame),
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
        


        # @ @ @ Serial Configuration Frame components @ @ @

        self.load_serial_button = tk.Button(self.serial_configuration_frame, 
                                                    text="Load Ports", 
                                                    command=self.load_ports,
                                                    height=2, 
                                                    width=20)

        self.combo_serial = ttk.Combobox(self.serial_configuration_frame)
        self.combo_serial.bind('<<ComboboxSelected>>', self.update_label_serial_port)

        self.selected_port_name_label = tk.Label(self.serial_configuration_frame,
                                                 text="NONE")
        
        self.selected_port_desc_label = tk.Label(self.serial_configuration_frame,
                                                 text="...")
        
        self.serial_baudrate = tk.StringVar(self.root)
        self.serial_baudrate.set("9600")
        
        self.baudrate_entry = tk.Entry(self.serial_configuration_frame, 
                                       textvariable=self.serial_baudrate,
                                       validate="key",
                                       validatecommand=(self.root.register(self.baudrate_entry_number_validation), "%P"))
        
        self.update_serial_configuration_button = tk.Button(self.serial_configuration_frame,
                                                             text="Update",
                                                             command=self.update_serial_configuration)
        

        self.home_serial_configuration_button = tk.Button(self.serial_configuration_frame, 
                                                          text="Return", 
                                                          command=lambda:self.frame_packer(self.main_frame))



        # @ @ @ Single Command Frame components @ @ @

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



        # @ @ @ Multiple Commands Frame components @ @ @

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
        
        # ----------------------------------
        # SECTION: COMPONENTS PACKING.
        # ----------------------------------

        self.serial_configuration_button.pack(pady=10)
        self.single_command_option_button.pack(pady=40)
        self.multiple_commands_window_button.pack(pady=50)

        self.load_serial_button.pack()
        self.selected_port_name_label.pack()
        self.selected_port_desc_label.pack()
        self.combo_serial.pack()
        self.baudrate_entry.pack()
        self.update_serial_configuration_button.pack(pady=10)
        self.home_serial_configuration_button.pack()
        
        self.knob.pack(pady=10)
        self.combo_joint.pack(pady=10)
        self.send_single_button.pack(pady=50)
        self.home_single_button.pack(pady=100)

        self.knob_q1.pack(pady=10, padx=10)
        self.knob_q2.pack(pady=20, padx=10)
        self.knob_q3.pack(pady=30, padx=10)
        self.send_multiple_button.pack(pady=100)
        self.home_multiple_button.pack(pady=10)

        # ----------------------------------
        # SECTION: FRAMES ORGANIZATION.
        # ----------------------------------

        self.frames = [
            self.main_frame,
            self.serial_configuration_frame,
            self.single_command_frame,
            self.multiple_command_frame
        ]

        self.main_frame.pack()

    # ||||||||||||||||||||||||||||||||||||||||||
    # MAIN METHODS OF THE CLASS.
    # ||||||||||||||||||||||||||||||||||||||||||

    # ----------------------------------
    # SECTION: 
    # ----------------------------------

    def load_ports(self):
        '''
        The function is used by a button who loads and refresh the
        current available port list in order for these to be selected
        in the combobox (combo_serial).
        '''
        ports_data = serial_configuration.get_ports()
        
        self.available_ports_data = {}

        for port, description, _ in ports_data:
            self.available_ports_data[port] = description
        
        listed_ports = list(self.available_ports_data.keys())

        self.combo_serial.configure(values=listed_ports)

    # ------------------------------------------------------------------------

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
        
    # ------------------------------------------------------------------------

    def baudrate_entry_number_validation(self, new_value:str):
        if new_value.isdigit() or new_value == "":
            return True
        return False
    
    def update_serial_configuration(self):
        pass

    def frame_packer(self, selected_frame:tk.Frame):
        '''
        Function used to update the frame that is being selected.
        :selected_frame: is searched in the list of the available frames 
        in order to be loaded. Any other frame is forgoten from the root.
        '''
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
