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


''''''
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
        self.DOF_entry.bind("<<Increment>>", self.dof_modify_increase) # FIXME: Working prior.
        self.DOF_entry.bind("<<Decrement>>", self.dof_modify_decrease) # FIXME: Working prior.

        self.degrees_Checkbutton = ttk.Checkbutton(self, 
                                                   text='Degrees', 
                                                   command=self.degrees_toggle_checkbutton, # FIXME: Working prior.
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
            label.place(relx=self.start_x + col * self.step_x + 0.02, 
                        rely=self.start_y - self.step_y,
                        anchor='center', width=80)
            
        # Placing the heading for the Ranges.
        label = ttk.Label(self, text="Ranges", justify='center')
        label.place(relx=self.start_x - self.step_x * 3.5,
                    rely=self.start_y - self.step_y,
                    anchor='center', width=50)
        
        self.initial_ranges_entries_request()
        self.initial_parameters_entries_request()
        self.initial_pointer_buttons_request()
        
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # MAIN FUNCTIONS.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    # -----------------------------
    # @@@        General        @@@
    # -----------------------------
    def initial_ranges_entries_request(self):

        for row in range(0, self.robotic_properties.degrees_of_freedom):
            new_row = []

            for col in range(2):
                entry = self.create_entry_component(row, col, 'RANGE')
                new_row.append(entry)

            self.entries_ranges_table.append(new_row)


    # ------------------------------------------------


    def initial_parameters_entries_request(self):

        for row in range(0, self.robotic_properties.degrees_of_freedom):
            new_row = []

            for col in range(4):
                entry = self.create_entry_component(row, col, 'PARAMETER')
                new_row.append(entry)

            self.entries_parameters_table.append(new_row)


    # ------------------------------------------------


    def initial_pointer_buttons_request(self):

        for row in range(0, self.robotic_properties.degrees_of_freedom):
            button = self.create_button_component(row)

            self.button_actuator_table.append(button)
            
    # ------------------------------------------------

    def create_entry_component(self, row:int, col:int, type_request:str):
        
        idx = 0
        idy = 0
        value = 0

        # validate_numbers = self.register(True)#self.validate_entry) #TODO: Set the validate_entry function.
        
        entry = CustomEntry(self, row, col, type_request)
        
        idy = self.start_y + row * self.step_y

        if type_request == "RANGE":
            idx = self.start_x - self.step_x * 2 + col * self.step_x - 0.1
            
            value = self.robotic_properties.ranges[row, col]

        if type_request == "PARAMETER":
            idx = self.start_x + col * self.step_x
            
            value = self.robotic_properties.DH_parameters_table[row, col]
            
            # In case it is the entry for a configurated actuator.
            if col == self.robotic_properties.pointer_actuators[row]:
                entry.configure(style="dh_params_config.TEntry")


        entry.place(relx=idx, rely=idy, anchor='center', width=40)


        # Visualization as degrees instead of radians.
        #TODO: Implement this condition to transform.
        if self.robotic_properties.pointer_actuators[row] == 0 and self.degrees_state.get():
            value = np.rad2deg(value)

        entry.insert(0, value)
        return entry

    # ------------------------------------------------

    def create_button_component(self, row:int):
        button = ttk.Button(self)
        button.configure(command=partial(self.actuator_toggle_button, button, row))
        button.place(relx=self.start_x + 5 * self.step_x, 
                     rely=self.start_y + row * self.step_y, 
                     anchor='center', width=80)
        
        # Text configuration according to the current settings for the actuators.
        button.configure(text='Linear' if self.robotic_properties.pointer_actuators[row] else 'Rotatory')

        return button
    

    # -----------------------------
    # @@@ Increase/Decrease DOF @@@
    # -----------------------------

    def dof_modify_increase(self, _:tk.Event):
        # Verifying not passing the upper limit.
        if int(self.DOF_entry.get()) == self.robotic_properties.dof_upp_limit:
            return
        
        # Degrees of freedom increase.
        self.robotic_properties.degrees_of_freedom += 1

        # Setting the value for the new row.
        row = self.robotic_properties.degrees_of_freedom - 1 

        # Adding the new empty row for the DH parameters.        
        new_line = np.array([0,0,0,0])
        self.robotic_properties.DH_parameters_table = np.append(self.robotic_properties.DH_parameters_table, 
                                                                [new_line], axis=0)
        
        # Adding the new empty row for the ranges.
        new_line = np.array([0,0])
        self.robotic_properties.ranges = np.append(self.robotic_properties.ranges, 
                                                   [new_line], axis=0)
        
        # Adding another pointer to the vector.
        self.robotic_properties.pointer_actuators = np.append(self.robotic_properties.pointer_actuators, 0)
        
        # Add a new line to the table, add visual entries. (RANGES, PARAMS Y BUTTON)
        new_row_ranges = []
        new_row_params = []

        # Ranges
        for col in range(2):
            entry = self.create_entry_component(row, col, 'RANGE')
            new_row_ranges.append(entry)

        # Params
        for col in range(4):
            entry = self.create_entry_component(row, col, 'PARAMETER')
            new_row_params.append(entry)

        # Button
        button = self.create_button_component(row)
        
        self.entries_ranges_table.append(new_row_ranges)
        self.entries_parameters_table.append(new_row_params)
        self.button_actuator_table.append(button)


    def dof_modify_decrease(self, _:tk.Event):
        # Verifying not passing the inferior limit.
        if int(self.DOF_entry.get()) == self.robotic_properties.dof_inf_limit:
            return
        
        self.robotic_properties.degrees_of_freedom -= 1

        previous_last_row = self.robotic_properties.degrees_of_freedom
        
        # Removing last row for the DH parameters.  
        self.robotic_properties.DH_parameters_table = np.delete(self.robotic_properties.DH_parameters_table,
                                                                previous_last_row,
                                                                axis=0)
        
        # Removing last row for the ranges.  
        self.robotic_properties.ranges = np.delete(self.robotic_properties.ranges,
                                                   self.robotic_properties.degrees_of_freedom,
                                                   axis=0)
        
        # Removing the last pointer from the vector.
        self.robotic_properties.pointer_actuators = np.delete(self.robotic_properties.pointer_actuators, 
                                                              previous_last_row)

        for entry in self.entries_ranges_table[previous_last_row]:
            entry.destroy()

        for entry in self.entries_parameters_table[previous_last_row]:
            entry.destroy()

        self.button_actuator_table[previous_last_row].destroy()

        
        self.entries_ranges_table.pop()
        self.entries_parameters_table.pop()
        self.button_actuator_table.pop()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@ Toggle Actuator Selection @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def actuator_toggle_button(self, button:tk.Button, row:int):
        
        current_value = self.robotic_properties.pointer_actuators[row]

        # Toggle the variable with boolean logic and back to int.
        self.robotic_properties.pointer_actuators[row] = int(not(current_value))

        # Text configuration according to the current settings for the actuators.
        button.configure(text='Linear' if self.robotic_properties.pointer_actuators[row] else 'Rotatory')

        self.toggle_reset_entries(row)

    # ------------------------------------------------

    def toggle_reset_entries(self, row:int):
        # Pointer for the new parameter set as the actuator.
        pointer = int(self.robotic_properties.pointer_actuators[row])

        # Reset to the inferior range.
        self.entries_ranges_table[row][0].delete(0, tk.END)
        self.entries_ranges_table[row][0].insert(0,"0.0")
        self.robotic_properties.ranges[row, 0] = 0

        # Reset to the upper range.
        self.entries_ranges_table[row][1].delete(0, tk.END)
        self.entries_ranges_table[row][1].insert(0,"0.0")
        self.robotic_properties.ranges[row, 1] = 0

        # Reset of the new assigned parameter. Changing styles as well.
        self.entries_parameters_table[row][pointer].delete(0, tk.END)
        self.entries_parameters_table[row][pointer].insert(0,"0.0")
        self.entries_parameters_table[row][pointer].configure(style="dh_params_config.TEntry")
        self.entries_parameters_table[row][int(not pointer)].configure(style="default.TEntry")
        self.robotic_properties.DH_parameters_table[row, pointer] = 0


    # ------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@
    # @@@ Entry Validation @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@

    def entry_changes(self):
        pass

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@ Degrees/Radians Mode @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def degrees_toggle_checkbutton(self):
        self.toggle_angles_ranges()
        self.toggle_angles_params()
        
        

    def toggle_angles_ranges(self):
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            # In case the ranges are set for a linear actuator, not updating the row.
            if self.robotic_properties.pointer_actuators[row] == 1:
                continue

            value_inf_range = self.robotic_properties.ranges[row, 0]
            value_sup_range = self.robotic_properties.ranges[row, 1]

            if self.degrees_state.get():
                value_inf_range = np.rad2deg(value_inf_range)
                value_sup_range = np.rad2deg(value_sup_range)

            inf_range_entry = self.entries_ranges_table[row][0]
            sup_range_entry = self.entries_ranges_table[row][1]

            inf_range_entry.delete(0, tk.END)
            inf_range_entry.insert(0, value_inf_range)

            sup_range_entry.delete(0, tk.END)
            sup_range_entry.insert(0, value_sup_range)





    def toggle_angles_params(self):
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            value_theta = self.robotic_properties.DH_default_table[row, 0]
            value_alpha = self.robotic_properties.DH_default_table[row, 3]

            if self.degrees_state.get():
                value_theta = np.rad2deg(value_theta)
                value_alpha = np.rad2deg(value_alpha)

            theta_entry = self.entries_parameters_table[row][0]
            alpha_entry = self.entries_parameters_table[row][3]

            theta_entry.delete(0, tk.END)
            theta_entry.insert(0, value_theta)

            alpha_entry.delete(0, tk.END)
            alpha_entry.insert(0, value_alpha)
            

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # SECONDARY FUNCTIONS.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    
# TODO: Create 3 funtions for initial creation of the entries (Ranges, parameters and buttons, store in the arrays).


    
    

    


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class RoboticConfigurationFrame2(CustomGrame):
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
        self.DOF_entry.bind("<Key>", self.block_keys) # FIXME: Working prior.
        self.DOF_entry.bind("<<Increment>>", self.dof_increment) # FIXME: Working prior.
        self.DOF_entry.bind("<<Decrement>>", self.dof_decrement) # FIXME: Working prior.

        self.degrees_Checkbutton = ttk.Checkbutton(self, 
                                                   text='Degrees', 
                                                   command=self.degrees_visual_update, # FIXME: Working prior.
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

        # Starting methods.
        self.update_information() # FIXME: Working prior.


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # - - - - - - - - - - Methods - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def clean_screen(self):
        '''
        
        '''
        for row in self.entries_parameters_table:
            for entry in row:
                entry.destroy()

        for button in self.button_actuator_table:
            button.destroy()

        for col in self.entries_ranges_table:
            for entry in col:
                entry.destroy()

    # ------------------------------------------------
    def update_information(self):
        '''
        
        '''
        self.focus_out_update_table_values(None)
        self.update_visual_tables()

        # Updating the default configuration as well.
        self.robotic_properties.DH_default_table = self.robotic_properties.DH_parameters_table


    # ------------------------------------------------

    def update_visual_tables(self):
        '''
        
        '''

        print("UPDATE VISUAL DE TABLAS DE PROPERTIES. . . . ")

        # The table is first deleted to later be refreshed.
        self.clean_screen()

        # Entries tables are reset.
        self.entries_parameters_table = []
        self.entries_ranges_table = []
        self.button_actuator_table = []

        # Function registration for its binding.
        validate_numbers = self.register(self.validate_entry)

        # Looping each line according to the DOF.
        for row in range(0, self.robotic_properties.degrees_of_freedom):  
            # Empty row on each iteration.
            new_row_params = []
            new_row_ranges = []

            # Looping for the ranges of each line.
            for col in range(2):
                # Index for positional.
                idx = self.start_x - self.step_x * 2 + col * self.step_x
                idy = self.start_y + row * self.step_y

                # Entry for each of the range selection.
                range_entry = CustomEntry(self, row, col, 'ranges')
                range_entry.configure(validate='all', 
                                      validatecommand=(validate_numbers, "%P", "%V")) 
                range_entry.bind("<FocusOut>", self.focus_out_update_table_values)
                range_entry.place(relx=idx-0.1, rely=idy, anchor='center', width=40)

                # Extracting the value from the table.
                value = self.robotic_properties.ranges[row, col]

                # Visualization as degrees instead of radians.
                #TODO: Implement this condition to transform.
                if self.robotic_properties.pointer_actuators[row] == 0 and self.degrees_state.get():
                    value = np.rad2deg(value)

                range_entry.insert(0, value)
                new_row_ranges.append(range_entry)


            # Loop for the DH parameters table.
            for col in range(4):  
                
                # Index for positional.
                idx = self.start_x + col * self.step_x
                idy = self.start_y + row * self.step_y

                # Singular entry being created, bound and placed.
                entry = ttk.Entry(self, validate='all', 
                                  validatecommand=(validate_numbers, "%P", "%V"))
                entry.bind("<FocusOut>", self.focus_out_update_table_values)
                entry.place(relx=idx, rely=idy, anchor='center', width=40)
                
                # In case it is the entry for a configurated actuator.
                if col == self.robotic_properties.pointer_actuators[row]:
                    entry.configure(style="dh_params_config.TEntry")

                
                # Extracting the value from the table.
                value = self.robotic_properties.DH_parameters_table[row, col]

                # Visualization as degrees instead of radians.
                #TODO: Implement this condition to transform.
                if (col == 0 or col == 3) and self.degrees_state.get():
                    value = np.rad2deg(value)

                entry.insert(0, value)
                new_row_params.append(entry)


            # Final Button to change the pointer.
            button = ttk.Button(self)
            button.configure(command=partial(self.button_toggle_actuator, button, row))
            button.place(relx=self.start_x + 5 * self.step_x, 
                         rely=self.start_y + row * self.step_y, 
                         anchor='center', width=80)
            

            # Text configuration according to the current settings for the actuators.
            button.configure(text='Linear' if self.robotic_properties.pointer_actuators[row] else 'Rotatory')
            
            # Appending to the lists of components.
            self.button_actuator_table.append(button)
            self.entries_parameters_table.append(new_row_params)
            self.entries_ranges_table.append(new_row_ranges)


    # ------------------------------------------------

    def button_toggle_actuator(self, _:ttk.Button, row:int):
        '''
        
        '''
        current_value = self.robotic_properties.pointer_actuators[row]

        # Toggle the variable with boolean logic and back to int.
        self.robotic_properties.pointer_actuators[row] = int(not(current_value))

        self.update_information()

    # ------------------------------------------------
    
    def degrees_visual_update(self):
        '''
        
        '''
        self.update_visual_tables()


    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # - - - - - - - - - - Bindings- - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def block_keys(self, _):
        '''
        Event that triggers when any key is tried to be introduced. 
        Fully blocked functionality.
        '''
        return "break"
    
    # ------------------------------------------------

    def validate_entry(self, value:str, motive):
        '''
        This callback function makes the validation on the keystrokes for the entries.
        Not accepting letters or characters other than digits, points or minus sign.
        The callback also triggers the focus out update method, which makes other validations
        on the entries at the table the last second this is modified. 
        '''

        # Lost focus on the entry, verifying changes.
        if motive == "focusout":  
            self.focus_out_update_table_values(None)
            
            # FIXME: If required to optimize, save the value and compare it to see if changes had been made.
            return True
        
        # Characters validation.
        elif value == "":
            return True
        elif value == "-" and not value[1:].isdigit():
            return True
        elif value.replace(".", "", 1).isdigit() or (value.startswith("-") and value[1:].replace(".", "", 1).isdigit()):
            return True
        
        # Anything else is restricted.
        else:
            return False
    
    # ------------------------------------------------

    def focus_out_update_table_values(self, event:tk.Event):
        '''
        Binding callback called when the entries from the DH table has no parameters.
        It is also triggered when only the minus has been set, but there is no other number.
        Automatically sets the entry to zero.
        '''

        print("UPDATE DE VALORES CON ENTRIES...")

        # Updates validation in the ranges table.
        for row, pair in enumerate(self.entries_ranges_table):
            for col, entry in enumerate(pair):
                # Extracted for readability.
                value = entry.get()

                # Condition for the radians.
                condition_radians = self.robotic_properties.pointer_actuators[row] == 0 and self.degrees_state.get()

                # Emtpy entry.
                if value == "":
                    entry.insert(0,"0")

                # Only minus sign in the entry.
                if value == "-":
                    entry.delete(0, tk.END)
                    entry.insert(0,"0")

                # Not letting passing to the other sides (Min/Max).
                max_range = self.robotic_properties.ranges[row, 1]
                min_range = self.robotic_properties.ranges[row, 0]

                # In case the condition is met.
                # TODO: 
                if condition_radians:
                    value = str(np.deg2rad(float(value)))

                # In case the conversion is required, the radians mode is set.
                if col == 0 and float(value) > max_range:

                    entry.delete(0, tk.END)
                    entry.insert(0, max_range - 1)
                    self.robotic_properties.ranges[row, col] = max_range - 1 #FIXME: New implementations, check if these work.

                if col == 1 and float(value) < min_range:

                    entry.delete(0, tk.END)
                    entry.insert(0, min_range + 1)
                    self.robotic_properties.ranges[row, col] = min_range - 1 

                # Once verified, making the updates.
                self.robotic_properties.ranges[row, col] = value #FIXME:


        # Updates validation in the DH parameters table.
        for row, line_entries in enumerate(self.entries_parameters_table):
            for col, entry in enumerate(line_entries):
                
                # Extracted for readability.
                value = entry.get()

                # Emtpy entry.
                if value == "":
                    entry.insert(0,"0")

                # Only minus sign in the entry.
                if value == "-":
                    entry.delete(0, tk.END)
                    entry.insert(0,"0")

                #TODO: Implement the update.
                if (col == 0 and col == 3) and self.degrees_state.get():
                    value = str(np.deg2rad(float(value)))
                    
                # Out of ranges bounds. Only verified for parameters of actuators.
                if col == self.robotic_properties.pointer_actuators[row]:
                    min_range = self.robotic_properties.ranges[row, 0]
                    max_range = self.robotic_properties.ranges[row, 1]

                    if float(value) < min_range:
                        entry.delete(0, tk.END)
                        entry.insert(0, min_range)

                    if float(value) > max_range:
                        entry.delete(0, tk.END)
                        entry.insert(0, max_range)

                # Once verified, making the updates.
                self.robotic_properties.DH_parameters_table[row, col] = value
        
    # ------------------------------------------------
    
    def dof_increment(self, _):
        '''
        If the entry for the Degrees of Freedom configuration is incremented, the robotics
        parameters is updated, as well for the DH table. Visually, a new row is added as well.
        This new row has the default values set to zero. The established limits in the 
        robotic properties can not be passed. The pointer to the actuator and the list for the
        ranges are also updated.
        '''

        # Verifying not passing the upper limit.
        if int(self.DOF_entry.get()) == self.robotic_properties.dof_upp_limit:
            return

        self.robotic_properties.degrees_of_freedom += 1

        # Adding the new empty row for the DH parameters.        
        new_line = np.array([0,0,0,0])
        self.robotic_properties.DH_parameters_table = np.append(self.robotic_properties.DH_parameters_table, 
                                                                [new_line], axis=0)
        
        # Adding the new empty row for the ranges.
        new_line = np.array([0,0])
        self.robotic_properties.ranges = np.append(self.robotic_properties.ranges, 
                                                   [new_line], axis=0)
        
        # Adding another pointer to the vector.
        self.robotic_properties.pointer_actuators = np.append(self.robotic_properties.pointer_actuators, 0)
        
        # Updating the default DH table values.
        self.robotic_properties.DH_default_table = self.robotic_properties.DH_parameters_table

        # Self visual table is also updated with these changes.
        self.update_visual_tables()

    # ------------------------------------------------    
    
    def dof_decrement(self, _):
        '''
        If the entry for the Degrees of Freedom configuration is decreased, the robotics
        parameters is updated, as well for the DH table. Visually, the last row is deleted.
        The established limits in the robotic properties can not be passed. The pointer to 
        the actuator and the list for the ranges are also updated.
        '''
        # Verifying not passing the inferior limit.
        if int(self.DOF_entry.get()) == self.robotic_properties.dof_inf_limit:
            return
        
        self.robotic_properties.degrees_of_freedom -= 1

        # Removing last row for the DH parameters.  
        self.robotic_properties.DH_parameters_table = np.delete(self.robotic_properties.DH_parameters_table,
                                                                self.robotic_properties.degrees_of_freedom,
                                                                axis=0)
        
        # Removing last row for the ranges.  
        self.robotic_properties.ranges = np.delete(self.robotic_properties.ranges,
                                                   self.robotic_properties.degrees_of_freedom,
                                                   axis=0)
        
        # Removing the last pointer from the vector.
        self.robotic_properties.pointer_actuators = np.delete(self.robotic_properties.pointer_actuators, 
                                                              self.robotic_properties.degrees_of_freedom)
        
        # Updating the default DH table values.
        self.robotic_properties.DH_default_table = self.robotic_properties.DH_parameters_table
        
        # Self visual table is also updated with these changes.
        self.update_visual_tables()
        



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
