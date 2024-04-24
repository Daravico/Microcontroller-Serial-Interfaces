import tkinter as tk
from tkinter import ttk
from serial import Serial
import serial_configuration
from robot_calculations import RoboticProperties
import numpy as np

# REMOVE THE OPTION OF SINGLE COMMAND SEND. CHANGE THE NAME OF 
# THE OTHER VARIABLES AND ADJUST THE LOADING FRAMES TO HAVE SHORTER NAMES AND LESS FUNCTIONS/PARAMETERS.

# CHANGE SLIDE BARS FOR KNOBS. ttk.

# Include continous mode. If checklist selected, the updates should be performed each time the knob is moved.

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
        self.send_command_frame = tk.Frame(self.root)
        self.robotics_details_frame = tk.Frame(self.root, background='#DAF0D2')

        # Other Variables.
        self.serial_baudrate_value = tk.StringVar(self.root)
        self.serial_baudrate_value.set("9600")

        self.joint_values = [0, 90, 0]

        # DH Parameters and Homogeneous Matrix variables.
        # CONSIDER OR MIGHT NOT CONSIDER CREATING THESE WITH SELF (NOT USER AFTER THE CONSTURCTOR IS CALLED, THESE ARE STORED SEPARATELY)
        # Note: 'q' is set to the default value at the start of the program <--------------------- YET TO 
        # IMPLEMENT, SEND THE COMMANDS ON START.
        q = [0,         np.pi/2,     0]
        d = [1,         0,           0]
        l = [0,         5,           3]
        A = [np.pi/2,   0,           0]
        
        ranges = [[-90, 90], [0, 90], [0, 90]]

        self.robotic_properties_3DOF = RoboticProperties(q, d, l, A, ranges)

        # /////////////////////////////////////////////////////////////////////
        #            SECTION: COMPONENTS INITIALIZATION AND PACKING.
        # ////////////////////////////////////////////////////////////////////

        # @ @ @ Main Frame components @ @ @

        self.serial_configuration_button = tk.Button(self.main_frame,
                                                     text="Serial Configuration",
                                                     command=lambda:self.frame_packer(self.serial_configuration_frame),
                                                     height=2,
                                                     width=20)
        
        self.send_commands_frame_button = tk.Button(self.main_frame, 
                                                    text="Multiple Commands", 
                                                    command=lambda:self.send_command_frame_packer(self.send_command_frame),
                                                    height=2, 
                                                    width=20)
        
        # Main frame components packing.
        self.serial_configuration_button.pack(pady=5)
        self.send_commands_frame_button.pack(pady=5)

        # -------------------------------------------------------------------------------
        
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
        
        self.baudrate_entry = tk.Entry(self.serial_configuration_frame, 
                                       textvariable=self.serial_baudrate_value,
                                       validate="key",
                                       validatecommand=(self.root.register(self.baudrate_entry_number_validation), "%P"))
        
        self.update_serial_configuration_button = tk.Button(self.serial_configuration_frame,
                                                             text="Update",
                                                             command=self.update_serial_configuration)
        
        self.home_serial_configuration_button = tk.Button(self.serial_configuration_frame, 
                                                          text="Return", 
                                                          command=lambda:self.frame_packer(self.main_frame))

        # Serial Configuration frame components packing.
        self.load_serial_button.pack(pady=5)
        self.selected_port_name_label.pack(pady=5)
        self.selected_port_desc_label.pack(pady=5)
        self.combo_serial.pack(pady=5)
        self.baudrate_entry.pack(pady=5)
        self.update_serial_configuration_button.pack(pady=5)
        self.home_serial_configuration_button.pack(pady=5)

        # -------------------------------------------------------------------------------

        # @ @ @ Commands Sender Frame components @ @ @

        self.knob_q1 = tk.Scale(self.send_command_frame, 
                                from_=-90, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                label='Q1')
        
        self.knob_q2 = tk.Scale(self.send_command_frame, 
                                from_=0, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                label='Q2')
        
        self.knob_q3 = tk.Scale(self.send_command_frame, 
                                from_=0, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                label='Q3')
        
        self.send_command_button = tk.Button(self.send_command_frame, 
                                     text="Send Command", 
                                     command=self.send_commands)

        self.home_button = tk.Button(self.send_command_frame, 
                                     text="Return", 
                                     command=lambda:self.frame_packer(self.main_frame))
        
        # Command sender frame packing.
        self.knob_q1.pack(pady=5, padx=10)
        self.knob_q2.pack(pady=5, padx=10)
        self.knob_q3.pack(pady=5, padx=10)
        self.send_command_button.pack(pady=5)
        self.home_button.pack(pady=5)

        # -------------------------------------------------------------------------------    

        # @ @ @ Robotics details components @ @ @

        self.dh_table = ttk.Treeview(self.robotics_details_frame, columns=("a", "alpha", "d", "theta"), show="headings")

        self.dh_table.heading("a", text="a")
        self.dh_table.column("a", minwidth=0, width=100, stretch=tk.NO)

        self.dh_table.heading("alpha", text="α")
        self.dh_table.column("alpha", minwidth=0, width=100, stretch=tk.NO)

        self.dh_table.heading("d", text="d")
        self.dh_table.column("d", minwidth=0, width=100, stretch=tk.NO)

        self.dh_table.heading("theta", text="θ")
        self.dh_table.column("theta", minwidth=0, width=100, stretch=tk.NO)

        self.homogeneous_table = ttk.Treeview(self.robotics_details_frame, columns=(" ", " ", " ", " "), show="headings")
        self.homogeneous_table.heading(" ", text=" ")

        self.position_table = ttk.Treeview(self.robotics_details_frame, columns=("X", "Y", "Z"), show="headings")
        self.position_table.heading("X", text="X")
        self.position_table.heading("Y", text="Y")
        self.position_table.heading("Z", text="Z")
        
        # Robotics details frame packing.
        self.dh_table.pack(side='top', pady=5)
        self.homogeneous_table.pack(side='bottom', pady=5)
        self.position_table.pack(side='bottom', pady=5)


        for count, row in enumerate(self.robotic_properties_3DOF.DH_table):
            self.dh_table.insert("", "end", iid=count, values=list(row))
  
        # -------------------------------------------------------------------------------    


    

        # ----------------------------------
        # SECTION: FRAMES ORGANIZATION.
        # ----------------------------------

        self.frames = [
            self.main_frame,
            self.serial_configuration_frame,
            self.send_command_frame,
            self.robotics_details_frame
        ]

        self.main_frame.pack()

    # ||||||||||||||||||||||||||||||||||||||||||
    # MAIN METHODS OF THE CLASS.
    # ||||||||||||||||||||||||||||||||||||||||||

    # ----------------------------------
    # SECTION: SERIAL CONFIGURATION METHODS.
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
        '''
        Callback function that is called when a new entry is set for the baudrate.
        This confirms if it is a number or a blank space in order to avoid chars in
        the value required as int.
        '''
        if new_value.isdigit() or new_value == "":
            return True
        return False
    
    # ------------------------------------------------------------------------
    
    def update_serial_configuration(self):
        '''
        Casting the value of the variable holding the baudrate from the entry
        to an integer and updating the configuration for the serial port.
        '''
        if self.combo_serial.get() == None or self.combo_serial.get() == "":
            print("No changes")
            return
        
        self.serial_conn.port = self.combo_serial.get()
        self.serial_conn.baudrate = int(self.serial_baudrate_value.get())
        
        print(f'PORT: {self.serial_conn.port} | BAUDRATE: {self.serial_conn.baudrate}')

    # ----------------------------------
    # SECTION: FRAME UPDATE METHODS.
    # ----------------------------------

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

    def send_command_frame_packer(self, selected_frame:tk.Frame):
        for frame in self.frames:

            if frame == self.robotics_details_frame:
                frame.pack(side="right")
                continue

            if frame != selected_frame:
                frame.pack_forget()
                continue

            frame.pack(side="left")

            
    # ----------------------------------
    # SECTION: SENDING COMMANDS OPTIONS.
    # ----------------------------------

    def send_commands(self):
        Q1_value = self.knob_q1.get()
        Q2_value = self.knob_q2.get()
        Q3_value = self.knob_q3.get()

        command = f'M#Q1-{Q1_value},Q2-{Q2_value},Q3-{Q3_value}'

        print(command)

    # oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo


if __name__ == '__main__':

    root = tk.Tk()
    root.title("Robot Serial Interface")
    root.geometry('1200x600')
    root.configure(background='#F0ECD2')
    control_gui = ControlGUI(root)

    root.mainloop()