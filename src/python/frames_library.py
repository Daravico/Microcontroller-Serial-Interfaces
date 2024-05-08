import numpy as np
import tkinter as tk
from tkinter import ttk
from typing import List
from serial_library import SerialObject
from robotic_library import RoboticProperties

from functools import partial

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

# TODO: Implement a method to check if the frame is direct or
# inverse kinematics to update details from the robotic properties.

class FrameHandler:
    '''
    Handles the loading of the frames required from the user inputs, separating the normal
    frames from the ones that are required to load some configurations and send information.
    '''
    def __init__(self):
        '''
        The constructor is only requried to have a list of the available frames, so that
        this can be easily organized and accessed in case any function is required from them.
        '''
        self.frames:List[CustomGrame] = [] 

    # ------------------------------------------------

    def frame_packer(self, frame_name:str):
        '''
        Function used to update the frame that is being selected. Normal frames are loaded into.
        '''
        for frame in self.frames:
            if frame.name != frame_name:
                frame.pack_forget()
                continue
            frame.pack(expand=True, fill='both')

    # ------------------------------------------------

    # FIXME: Fix this function, depending on the new implementations.
    # TODO: Posiblemente requiera recibir otro objeto para actualizar.
    def direct_kinematic_frame_packer(self, frame_name:str):
        '''
        This function handles the loading of the direct kinematics frame so that 
        the configurations from the robotic properties can be established prior to
        make modifications on this section of the code.
        '''
        for frame in self.frames:

            if frame == self.robotic_details_frame:
                frame.pack(side="right", anchor="center", expand=True, fill='both')
                continue

            # FIXME: Check from where this problem comes from.
            if frame.name != frame_name:
                frame.pack_forget()
                continue

            frame.pack(side="left", expand=True, fill='both')

    # ------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

# CUSTOMIZATIONS TO HOLD VALUES.

class CustomGrame(ttk.Frame):
    '''
    General class for the frames, inherited from tk.Frame to add some characteristics
    required by other classes, such as the name and the frame_handler asigned by the
    main window.
    '''
    def __init__(self, root:tk.Tk, name: str, frame_handler:FrameHandler):
        ttk.Frame.__init__(self, root)
        self.frame_handler = frame_handler 
        self.root = root
        self.name = name


class CustomEntry(ttk.Entry):
    '''
    
    '''
    def __init__(self, frame:tk.Frame, row:int, col:int, entry_type:str):
        ttk.Entry.__init__(self, frame)
        self.row = row
        self.col = col
        self.entry_type = entry_type

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class MainMenuFrame(CustomGrame):
    '''
    First frame that is loaded that redirects to the other available options
    for configurations and working setups.
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        CustomGrame.__init__(self, root, 'main_frame', frame_handler)


        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.serial_configuration_button = ttk.Button(self,
                                                     text="Serial Configuration",
                                                     command=lambda: frame_handler.frame_packer('serial_configuration_frame'),
                                                     padding=(5,15),
                                                     width=30)
        
        self.robotic_configuration_button = ttk.Button(self,
                                                      text="Robotic Configuration",
                                                      command=lambda: frame_handler.frame_packer('robotic_configuration_frame'),
                                                      padding=(5,15),
                                                      width=30)

        # TODO: Change for the other frame packer.
        self.direct_kinematics_frame_button = ttk.Button(self, 
                                                        text="Direct Kinematics", 
                                                        command=lambda: frame_handler.frame_packer('direct_kinematics_frame'),
                                                        padding=(5,15), 
                                                        width=30)
        
        # TODO: Change for the other frame packer.
        self.inverse_kinematics_frame_button = ttk.Button(self, 
                                                          text="Inverse Kinematics", 
                                                          command=lambda: frame_handler.frame_packer('inverse_kinematics_frame'),
                                                          padding=(5,15),
                                                          width=30)
        
        self.exit_window_button = ttk.Button(self, 
                                             text="Exit", 
                                             command=self.root.destroy,
                                             width=20, padding=(5,10))

        # Main frame components placing.
        self.serial_configuration_button.place(relx=0.5, rely=0.2, anchor='center')
        self.robotic_configuration_button.place(relx=0.5, rely=0.3, anchor='center')
        self.direct_kinematics_frame_button.place(relx=0.5, rely=0.4, anchor='center')
        self.inverse_kinematics_frame_button.place(relx=0.5, rely=0.5, anchor='center')
        self.exit_window_button.place(relx=0.5, rely=0.8, anchor='center')


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class SerialConfigurationFrame(CustomGrame):
    '''
    Frame that has functionalities to make modifications to the Serial Communication, as well
    for loading some variables related to this.
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler, serial_conn:SerialObject):
        CustomGrame.__init__(self, root, 'serial_configuration_frame', frame_handler)

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

        self.load_serial_button = ttk.Button(self, 
                                             text="Load Ports",
                                             command=self.load_ports,
                                             width=20, padding=(5,10))

        self.combo_serial = ttk.Combobox(self)
        
        self.combo_serial.bind('<<ComboboxSelected>>', self.update_label_serial_port)

        self.selected_port_name_label = ttk.Label(self,
                                                  text='NONE')
        
        self.selected_port_desc_label = ttk.Label(self,
                                                  text="...")
        
        # TODO: Add correct validations. Add the starting value.
        self.baudrate_entry = ttk.Entry(self, 
                                        textvariable=self.serial_baudrate_value,
                                        validate="key",
                                        validatecommand=(self.root.register(self.number_validation), "%P"))
        
        self.update_serial_configuration_button = ttk.Button(self, 
                                                             text="Update",
                                                             command=self.update_serial_configuration,
                                                             width=20, padding=(5,10))
        
        self.home_return_button = ttk.Button(self, 
                                            text="Return", 
                                            command=lambda: frame_handler.frame_packer('main_frame'),
                                            width=20, padding=(10,20))

        # Serial Configuration frame components placing.
        self.load_serial_button.place(relx=0.5, rely=0.2, anchor='center')
        self.selected_port_name_label.place(relx=0.5, rely=0.3, anchor='center')
        self.selected_port_desc_label.place(relx=0.5, rely=0.4, anchor='center')
        self.combo_serial.place(relx=0.5, rely=0.5, anchor='center')
        self.baudrate_entry.place(relx=0.5, rely=0.6, anchor='center')
        self.update_serial_configuration_button.place(relx=0.5, rely=0.7, anchor='center')
        self.home_return_button.place(relx=0.5, rely=0.8, anchor='center')

        # Loading the available ports.
        self.load_ports()

        if self.serial_conn.port != None and len(self.available_ports_data) != 0:
            self.selected_port_name_label.configure(text=self.serial_conn.port)
            self.selected_port_desc_label.configure(text=self.available_ports_data[self.serial_conn.port])
            

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

    def update_label_serial_port(self):
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


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # - - - - - - - - - - Bindings- - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def number_validation(self, new_value:str):
        '''
        Callback function that is called when a new entry is set for the baudrate.
        This confirms if it is a number or a blank space in order to avoid chars in
        the value required as int.
        '''
        if new_value.isdigit() or new_value == "":
            return True
        return False
    

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class RoboticConfigurationFrame(CustomGrame):
    '''
    
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler, robotic_properties: RoboticProperties):
        CustomGrame.__init__(self, root, 'robotic_configuration_frame', frame_handler)

        # Saving the information of the robotic properties. Futher changes are also updated.
        self.robotic_properties = robotic_properties

        # Table lists to be able to clean the screen by deleting these objects.
        self.entries_parameters_table:List[List[CustomEntry]] = []
        self.button_actuator_table:List[ttk.Button] = []
        self.entries_ranges_table:List[List[CustomEntry]] = []

        # Placing variables.
        self.start_x = 0.3
        self.start_y = 0.3
        self.step_x = 0.05
        self.step_y = 0.1

        # Visualization of degrees or radians.
        self.degrees_state = tk.BooleanVar()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.DOF_entry = ttk.Spinbox(self, from_=1, to=5)
        self.DOF_entry.set(self.robotic_properties.degrees_of_freedom)
        #self.DOF_entry.bind("<Key>", self.block_keys) # FIXME: Working prior.
        #self.DOF_entry.bind("<<Increment>>", self.dof_increment) # FIXME: Working prior.
        #self.DOF_entry.bind("<<Decrement>>", self.dof_decrement) # FIXME: Working prior.

        self.degrees_Checkbutton = ttk.Checkbutton(self, 
                                                   text='Degrees', 
                                                   #command=self.degrees_visual_update, # FIXME: Working prior.
                                                   variable=self.degrees_state)

        self.home_return_button = ttk.Button(self, 
                                            text="Return", 
                                            command=lambda: frame_handler.frame_packer('main_frame'),
                                            width=20, padding=(10,20))
        
        # Placing components.
        self.DOF_entry.place(relx=0.3, rely=0.1, anchor='center')
        self.degrees_Checkbutton.place(relx=0.4, rely=0.1, anchor='center')
        self.home_return_button.place(relx=0.3, rely=0.8, anchor='center')

        # Placing the headings for the DH table.
        headings = ['θ', 'd', 'a', 'α']
        for col, head in enumerate(headings):
            label = ttk.Label(self, text=head, justify='right')
            label.place(relx=self.start_x + col * self.step_x, 
                        rely=self.start_y - self.step_y,
                        anchor='center', width=80)
            
        # Placing the heading for the Ranges.
        label = ttk.Label(self, text="Ranges", justify='center')
        label.place(relx=self.start_x - self.step_x * 3.5,
                    rely=self.start_y - self.step_y,
                    anchor='center', width=50)
        

    def dof_modify_increase(self):
        pass



    def dof_modify_decrease(self):
        pass



    def actuator_toggle_button(self):
        pass



    def entry_changes(self):
        pass



    def degrees_toggle_checkbutton(self):
        pass


    def loop_ranges_request(self):
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            pass
            # for col in





# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class DirectKinematicsFrame(CustomGrame):
    '''
    
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        CustomGrame.__init__(self, root, 'direct_kinematics_frame', frame_handler)



        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.home_return_button = ttk.Button(self, 
                                            text="Return", 
                                            command=lambda: frame_handler.frame_packer('main_frame'),
                                            width=20, padding=(10,20))
        
        # Packing components.
        self.home_return_button.place(relx=0.5, rely=0.8, anchor='center')
        

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class InverseKinematicsFrame(CustomGrame):
    '''
    
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        CustomGrame.__init__(self, root, 'inverse_kinematics_frame', frame_handler)


        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.home_return_button = ttk.Button(self, 
                                            text="Return", 
                                            command=lambda: frame_handler.frame_packer('main_frame'),
                                            width=20, padding=(10,20))
        
        # Packing components.
        self.home_return_button.place(relx=0.5, rely=0.8, anchor='center')
