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
        self.frames:List[CustomFrame] = [] 

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

            # Placing the details of the parameters for the robotic configuration to the right.
            if frame.name == 'robotic_params_frame':
                frame.pack(side="right", anchor="center", expand=True, fill='both')
                continue

            # Anything other than the controller is omitted.
            if frame.name != frame_name:
                frame.pack_forget()
                continue

            # Placing the controller on the left.
            frame.pack(side="left", expand=True, fill='both')

    # ------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

# CUSTOMIZATIONS TO HOLD VALUES.

class CustomFrame(ttk.Frame):
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
    General class for the entries, inherited from ttk.Entry to add some characteristics
    required bu other classes, such as the row and column of the Entry and the type of
    details that it will be used for.
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

class MainMenuFrame(CustomFrame):
    '''
    First frame that is loaded that redirects to the other available options
    for configurations and working setups.
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        CustomFrame.__init__(self, root, 'main_frame', frame_handler)


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

        self.direct_kinematics_frame_button = ttk.Button(self, 
                                                        text="Direct Kinematics", 
                                                        command=lambda: frame_handler.direct_kinematic_frame_packer('direct_kinematics_frame'),
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

class SerialConfigurationFrame(CustomFrame):
    '''
    Frame that has functionalities to make modifications to the Serial Communication, as well
    for loading some variables related to this.
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler, serial_conn:SerialObject):
        CustomFrame.__init__(self, root, 'serial_configuration_frame', frame_handler)

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

class RoboticConfigurationFrame(CustomFrame):
    '''
    Frame that has functionalities to make modifications to the robotic parameters.
    Degrees or Radians visualization is available. 
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler, robotic_properties: RoboticProperties):
        CustomFrame.__init__(self, root, 'robotic_configuration_frame', frame_handler)

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

        self.DOF_entry = ttk.Spinbox(self, from_=self.robotic_properties.dof_inf_limit, to=self.robotic_properties.dof_upp_limit)
        self.DOF_entry.set(self.robotic_properties.degrees_of_freedom)
        self.DOF_entry.bind("<Key>", self.block_keys) 
        self.DOF_entry.bind("<<Increment>>", self.dof_modify_increase) 
        self.DOF_entry.bind("<<Decrement>>", self.dof_modify_decrease) 

        self.degrees_Checkbutton = ttk.Checkbutton(self, 
                                                   text='Degrees', 
                                                   command=self.degrees_toggle_checkbutton, 
                                                   variable=self.degrees_state)

        self.home_return_button = ttk.Button(self, 
                                            text="Return", 
                                            command=lambda: frame_handler.frame_packer('main_frame'),
                                            width=20, padding=(10,20))
        
        # Placing components.
        self.DOF_entry.place(relx=0.3, rely=0.1, anchor='center')
        self.degrees_Checkbutton.place(relx=0.4, rely=0.1, anchor='center')
        self.home_return_button.place(relx=0.8, rely=0.5, anchor='center')

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

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@        General        @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def initial_ranges_entries_request(self):
        '''
        Initial request to create the entries from the table designed for the ranges.
        '''
        # Looping rows.
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            new_row = []
            # Looping columns.
            for col in range(2):
                entry = self.create_entry_component(row, col, 'RANGE')
                new_row.append(entry)

            # Adding to the table.
            self.entries_ranges_table.append(new_row)


    # ------------------------------------------------

    def initial_parameters_entries_request(self):
        '''
        Initial request to create the entries from the table designed for the parameters.
        '''
        # Looping rows.
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            new_row = []
            # Looping columns.
            for col in range(4):
                entry = self.create_entry_component(row, col, 'PARAMETER')
                new_row.append(entry)

            # Adding to the table.
            self.entries_parameters_table.append(new_row)


    # ------------------------------------------------

    def initial_pointer_buttons_request(self):
        '''
        Initial request to create the entries from the table designed for the buttons.
        '''
        # Looping the vector.
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            button = self.create_button_component(row)

            #Adding to the list.
            self.button_actuator_table.append(button)
            

    # ------------------------------------------------

    def block_keys(self, _):
        '''
        Event that triggers when any key is tried to be introduced. 
        Fully blocked functionality.
        '''
        return "break"


    # ------------------------------------------------

    def create_entry_component(self, row:int, col:int, type_request:str):
        '''
        Request to create an entry. Row and column information is passed as a parameter in order to
        update the information from the tables. Depending on the type request, the entry is created 
        with certain characteristics.
        '''
        
        # Variables later used.
        idx = 0
        idy = self.start_y + row * self.step_y
        value = 0

        # Function to validate the correct entry used.
        validate_numbers = self.register(self.entry_validation) 
        
        # Entry creation with default values.
        entry = CustomEntry(self, row, col, type_request)
        entry.configure(validate="all", validatecommand=(validate_numbers, "%P", "%V"))
        
        # Additional configuration for range entries.
        if type_request == "RANGE":
            idx = self.start_x - self.step_x * 4 + col * self.step_x 
            entry.bind("<FocusOut>", lambda event, row=row, col=col: self.entry_ranges_focus_out(event, entry, row, col))
            value = self.robotic_properties.ranges[row, col]

        # Additional configuration for parameters entries.
        if type_request == "PARAMETER":
            idx = self.start_x + col * self.step_x
            entry.bind("<FocusOut>", lambda event, row=row, col=col: self.entry_params_focus_out(event, entry, row, col))
            value = self.robotic_properties.dh_params_save_table[row, col]
            
            # Styling in case it is the entry for a configurated actuator.
            if col == self.robotic_properties.pointer_actuators[row]:
                entry.configure(style="dh_params_config.TEntry")

        # Placing and inserting the value.
        entry.place(relx=idx, rely=idy, anchor='center', width=40)
        entry.insert(0, value)

        # Returning to be appended to the list.
        return entry


    # ------------------------------------------------

    def create_button_component(self, row:int):
        '''
        Request to create the button to toggle the actuator type. The row details is passed to 
        locate the object in the vector list and modify any required detail.
        '''
        # Button creation and initial configuration.
        button = ttk.Button(self)
        button.configure(command=partial(self.actuator_toggle_button, button, row))
        button.place(relx=self.start_x + 5 * self.step_x, 
                     rely=self.start_y + row * self.step_y, 
                     anchor='center', width=80)
        
        # Text configuration according to the current settings for the actuators.
        button.configure(text='Linear' if self.robotic_properties.pointer_actuators[row] else 'Rotatory')

        # Return button to be appended.
        return button
    

    # -----------------------------
    # @@@ Increase/Decrease DOF @@@
    # -----------------------------

    def dof_modify_increase(self, _:tk.Event):
        '''
        Request to increase the degrees of freedom from the configuration. The Superior
        Limit can not be passed. Elements from the tables are modified, adding them to both
        the configuration and the visuals of the table.
        '''
        # Verifying not passing the upper limit.
        if int(self.DOF_entry.get()) == self.robotic_properties.dof_upp_limit:
            return
        
        # Degrees of freedom increase, setting the row index.
        self.robotic_properties.degrees_of_freedom += 1
        row = self.robotic_properties.degrees_of_freedom - 1 

        # Adding the new empty row for the DH parameters.        
        new_line = np.array([0,0,0,0])
        self.robotic_properties.dh_params_save_table = np.append(self.robotic_properties.dh_params_save_table, 
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

        # Ranges entries creation.
        for col in range(2):
            entry = self.create_entry_component(row, col, 'RANGE')
            new_row_ranges.append(entry)

        # Params entries creation.
        for col in range(4):
            entry = self.create_entry_component(row, col, 'PARAMETER')
            new_row_params.append(entry)

        # Button creation.
        button = self.create_button_component(row)
        
        # Adding to the list.
        self.entries_ranges_table.append(new_row_ranges)
        self.entries_parameters_table.append(new_row_params)
        self.button_actuator_table.append(button)


    # ------------------------------------------------

    def dof_modify_decrease(self, _:tk.Event):
        '''
        Request to decrease the degrees of freedom from the configuration. The Inferior
        Limit can not be passed. Elements from the tables are modified, removing the last line
        from both the visual tables and the configuration.
        '''
        # Verifying not passing the inferior limit.
        if int(self.DOF_entry.get()) == self.robotic_properties.dof_inf_limit:
            return
        
        # Decreasing the DOF, saving the index for the last row.
        self.robotic_properties.degrees_of_freedom -= 1
        previous_last_row = self.robotic_properties.degrees_of_freedom
        
        # Removing last row for the DH parameters.  
        self.robotic_properties.dh_params_save_table = np.delete(self.robotic_properties.dh_params_save_table,
                                                                previous_last_row,
                                                                axis=0)
        
        # Removing last row for the ranges.  
        self.robotic_properties.ranges = np.delete(self.robotic_properties.ranges,
                                                   self.robotic_properties.degrees_of_freedom,
                                                   axis=0)
        
        # Removing the last pointer from the vector.
        self.robotic_properties.pointer_actuators = np.delete(self.robotic_properties.pointer_actuators, 
                                                              previous_last_row)

        # Ranges entries removing.
        for entry in self.entries_ranges_table[previous_last_row]:
            entry.destroy()

        # Params entries removing.
        for entry in self.entries_parameters_table[previous_last_row]:
            entry.destroy()

        # Removing the button.
        self.button_actuator_table[previous_last_row].destroy()

        # Removing from the list. 
        self.entries_ranges_table.pop()
        self.entries_parameters_table.pop()
        self.button_actuator_table.pop()

    
    # ------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@ Toggle Actuator Selection @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def actuator_toggle_button(self, button:tk.Button, row:int):
        '''
        This method changes the current state of the vector that determinates the parameter 
        assigned for the actuator (Rotatory or linear). The color style is also changed, and the 
        entries affected (Both ranges and parameter) are reset to zero.
        '''
        # Getting the index for the current parameter of the actuator configuration.
        current_value = self.robotic_properties.pointer_actuators[row]

        # Toggle the variable with boolean logic and back to int.
        self.robotic_properties.pointer_actuators[row] = int(not(current_value))

        # Text configuration according to the current settings for the actuators.
        button.configure(text='Linear' if self.robotic_properties.pointer_actuators[row] else 'Rotatory')

        # Calling method to reset entries.
        self.toggle_reset_entries(row)


    # ------------------------------------------------

    def toggle_reset_entries(self, row:int):
        '''
        Resetting the affected entries back to zero in order to establish the new details
        of the ranges and parameter value manually.
        '''
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
        self.robotic_properties.dh_params_save_table[row, pointer] = 0

        # The active table is also set.
        self.robotic_properties.dh_params_active_table = self.robotic_properties.dh_params_save_table


    # ------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@
    # @@@ Entry Validation @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@

    def entry_validation(self, value:str, _:str):
        '''
        Validation of a proper entry inserted in the cells. Numbers are only accepted, as well for 
        having an empty entry and the minus sign at the start of the number to represent negative values.
        '''

        # Individual conditions. Anything outside these will not be accepted.
        if value == "" or value.replace(".", "", 1).isdigit():
            return True
        elif value == "-":  
            return True
        elif value.replace(".", "", 1).isdigit() or (value.startswith("-") and value[1:].replace(".", "", 1).isdigit()):
            return True
        else:
            return False


    # ------------------------------------------------

    def entry_ranges_focus_out(self, _:tk.Event, entry:CustomEntry, row:int, col:int):
        '''
        Function callback used when the entry for the ranges is out of focus, meaning that no more changes 
        will be performed. The verification makes sure that ranges are taken in consideration, as well for
        leaving a numeric representation inside the cell.
        '''
        # Extracting the current range limits. 
        max_range = self.robotic_properties.ranges[row, 1]
        min_range = self.robotic_properties.ranges[row, 0]

        # Entry value.
        value = entry.get()

        # Index for the row affected. The value for the entry of the parameter is also extracted.
        param_actuator_affected = int(self.robotic_properties.pointer_actuators[row])
        value_parameter = self.robotic_properties.dh_params_save_table[row, param_actuator_affected]

        # Empty condition.
        if value == "":
            value = 0
            entry.insert(0,"0.0")

        # Only minus condition.
        elif value == "-":
            value = 0
            entry.delete(0, tk.END)
            entry.insert(0,"0.0")

        # Numeric value validations.
        value = float(value)

        # Degrees mode ON.
        if self.degrees_state.get() and param_actuator_affected == 0:
            value = np.deg2rad(value)
        
        # Max limit passed verification.
        if col == 0 and value > max_range:
            value = max_range - 1
            entry.delete(0, tk.END)
            if self.degrees_state.get():
                entry.insert(0, np.rad2deg(value))
            else:
                entry.insert(0, value)

        # Min limit verification.
        elif col == 1 and value < min_range:
            value = min_range + 1
            entry.delete(0, tk.END)
            if self.degrees_state.get():
                entry.insert(0, np.rad2deg(value))
            else:
                entry.insert(0, value)
        
        # Updating configuration for robot.
        self.robotic_properties.ranges[row][col] = value

        # Updating the ranges for the next function.
        max_range = self.robotic_properties.ranges[row, 1]
        min_range = self.robotic_properties.ranges[row, 0]
        
        # Adjusting the parameter to a middle point of the ranges if required.
        if value_parameter < min_range or value_parameter > max_range:
            value_parameter = (min_range + max_range) / 2

            # Entry variable modificaton.
            entry_parameter = self.entries_parameters_table[row][param_actuator_affected]
            entry_parameter.delete(0, tk.END)
            if self.degrees_state.get():
                entry_parameter.insert(0, np.rad2deg(value_parameter))
            else:
                entry_parameter.insert(0, value_parameter)
            
            # The active table is also set.
            self.robotic_properties.dh_params_active_table = self.robotic_properties.dh_params_save_table
  

    # ------------------------------------------------

    def entry_params_focus_out(self, _:tk.Event, entry:CustomEntry, row:int, col:int):
        '''
        Function callback used when the entry for the params is out of focus, meaning that no more changes 
        will be performed. The verification makes sure that ranges are taken in consideration, as well for
        leaving a numeric representation inside the cell.
        '''
        # Entry value.
        value = entry.get()

        # Extracting the current range limits.
        max_range = self.robotic_properties.ranges[row, 1]
        min_range = self.robotic_properties.ranges[row, 0]

        # Empty condition.
        if value == "":
            value = 0
            entry.insert(0,"0.0")

        # Only minus condition.
        elif value == "-":
            value = 0
            entry.delete(0, tk.END)
            entry.insert(0,"0.0")

        # Numeric value validations.
        value = float(value)

        # Degrees mode ON.
        if self.degrees_state.get() and (col == 0 or col == 3):
            value = np.deg2rad(value)

        # Max limit passed verification.
        if col == 0 and value > max_range:
            value = max_range
            entry.delete(0, tk.END)
            if self.degrees_state.get():
                entry.insert(0, np.rad2deg(value))
            else:
                entry.insert(0, value)

        # Min limit passed verification.
        elif col == 0 and value < min_range:
            value = min_range
            entry.delete(0, tk.END)
            if self.degrees_state.get():
                entry.insert(0, np.rad2deg(value))
            else:
                entry.insert(0, value)

        # Updating configuration for robot.
        self.robotic_properties.dh_params_save_table[row][col] = value

        # The active table is also set.
        self.robotic_properties.dh_params_active_table = self.robotic_properties.dh_params_save_table


    # ------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@ Degrees/Radians Mode @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def degrees_toggle_checkbutton(self):
        '''
        Function that calls the corresponding methods to perform the modification of 
        the available cells from degrees to radians or backwards.
        '''
        self.toggle_angles_ranges()
        self.toggle_angles_params()
        

    # ------------------------------------------------

    def toggle_angles_ranges(self):
        '''
        Method to check each of the rows and, in case the configuration states it, the 
        visual table for the ranges is updated to degrees or radians mode, depending 
        on the state of the checkbutton.
        '''
        # Looping through rows.
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            # In case the ranges are set for a linear actuator, not updating the row.
            if self.robotic_properties.pointer_actuators[row] == 1:
                continue
            
            # Extracting the limits.
            value_inf_range = self.robotic_properties.ranges[row, 0]
            value_sup_range = self.robotic_properties.ranges[row, 1]

            # Degrees mode ON.
            if self.degrees_state.get():
                value_inf_range = np.rad2deg(value_inf_range)
                value_sup_range = np.rad2deg(value_sup_range)

            # Entries objects.
            inf_range_entry = self.entries_ranges_table[row][0]
            sup_range_entry = self.entries_ranges_table[row][1]

            # Updating inferior limit entry.
            inf_range_entry.delete(0, tk.END)
            inf_range_entry.insert(0, value_inf_range)

            # Updating superior limit entry.
            sup_range_entry.delete(0, tk.END)
            sup_range_entry.insert(0, value_sup_range)


    # ------------------------------------------------

    def toggle_angles_params(self):
        '''
        Method to check each of the rows and, in case the configuration states it, the 
        visual table for the parameters is updated to degrees or radians mode, depending 
        on the state of the checkbutton.
        '''
        # Looping through rows.
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            value_theta = self.robotic_properties.dh_params_active_table[row, 0]
            value_alpha = self.robotic_properties.dh_params_active_table[row, 3]

            # Degrees mode ON.
            if self.degrees_state.get():
                value_theta = np.rad2deg(value_theta)
                value_alpha = np.rad2deg(value_alpha)

            # Entries objects.
            theta_entry = self.entries_parameters_table[row][0]
            alpha_entry = self.entries_parameters_table[row][3]

            # Updating theta entry.
            theta_entry.delete(0, tk.END)
            theta_entry.insert(0, value_theta)

            # Updating alpha entry.
            alpha_entry.delete(0, tk.END)
            alpha_entry.insert(0, value_alpha)
            

    # ------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class RoboticParamsFrame(CustomFrame):
    '''
    
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler, robotic_properties:RoboticProperties):
        CustomFrame.__init__(self,root, 'robotic_params_frame', frame_handler)

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class DirectKinematicsFrame(CustomFrame):
    '''
    
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler, robotic_properties:RoboticProperties, robotic_params_frame:RoboticParamsFrame):
        CustomFrame.__init__(self, root, 'direct_kinematics_frame', frame_handler)

        self.robotic_properties = robotic_properties

        self.continous_mode_state = tk.BooleanVar()
        self.continous_mode_state.set(False)

        scales_table:List[ttk.Scale] = []

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.continous_mode_checkbutton = ttk.Checkbutton(self, 
                                                         text='Auto',
                                                         command=None,
                                                         variable=self.continous_mode_state)



        self.send_command_button = ttk.Button(self, 
                                     text="Send Command", 
                                     command=None)

        self.home_return_button = ttk.Button(self, 
                                            text="Return", 
                                            command=lambda: frame_handler.frame_packer('main_frame'),
                                            width=20, padding=(10,20))
        
        # Placing components.
        self.continous_mode_checkbutton.place(relx=0.5, rely=0.15, anchor='center')
        self.home_return_button.place(relx=0.85, rely=0.15, anchor='center', width=150, height=50)
        self.send_command_button.place(relx=0.15, rely=0.15, anchor='center', width=150, height=50)

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # MAIN FUNCTIONS.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def initial_params_request(self):
        pass

    def initial_scales_request(self):
        pass

    def create_scale_component(self):
        pass
        
    def default_position_request(self):
        pass

    def send_command_request(self):
        pass


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

class InverseKinematicsFrame(CustomFrame):
    '''
    
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler, robotic_properties:RoboticProperties):
        CustomFrame.__init__(self, root, 'inverse_kinematics_frame', frame_handler)

        self.robotic_properties = robotic_properties

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

class GuidedProgrammingFrame(CustomFrame):
    '''
    
    '''
    def __init__(self, root:tk.Tk, frame_handler:FrameHandler):
        CustomFrame.__init__(self, root, 'guided_programming_frame', frame_handler)


        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.home_return_button = ttk.Button(self, 
                                            text="Return", 
                                            command=lambda: frame_handler.frame_packer('main_frame'),
                                            width=20, padding=(10,20))
        
        # Packing components.
        self.home_return_button.place(relx=0.5, rely=0.8, anchor='center')
        
