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
    # - - - - - - -Tested New Methods - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    def full_loop_iteration(self):
        # TODO: If prior configurations are required.
        pass
        #for row, line in 


    def update_dh_table(self):
        pass

    def update_rg_table(self):
        pass

    def refresh_visual_table_dh(self):
        pass

    def refresh_visual_table_rg(self):
        pass


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
        
