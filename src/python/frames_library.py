import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb

import numpy as np
from functools import partial

from serial_library import SerialObject
from robotic_library import RoboticProperties

from typing import List

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class FrameHandler:
    """
    Handles the loading of the frames required from the user inputs, separating the normal
    frames from the ones that are required to load some configurations and send information.
    """

    def __init__(self, serial_conn:SerialObject):
        """
        The constructor is only requried to have a list of the available frames, so that
        this can be easily organized and accessed in case any function is required from them.
        """
        self.frames: List[CustomFrame] = []
        self.serial_conn = serial_conn
    # ------------------------------------------------

    def frame_packer(self, frame_name: str):
        """
        Function used to update the frame that is being selected. Normal frames are loaded into.
        """
        # Closing the serial connection in any frame other than the DK Frame.
        self.serial_conn.close()

        for frame in self.frames:
            if frame.name != frame_name:
                frame.pack_forget()
                continue
            frame.pack(expand=True, fill="both")

    # ------------------------------------------------

    def direct_kinematic_frame_packer(self, frame_name: str):
        """
        This function handles the loading of the direct kinematics frame so that
        the configurations from the robotic properties can be established prior to
        make modifications on this section of the code.
        """
        # Opening the serial Connection in order to send instructions.
        self.serial_conn.open()

        for frame in self.frames:

            # Placing the details of the parameters for the robotic configuration to the right.
            if frame.name == "robotic_params_frame":
                frame.pack(side="right", anchor="center", expand=True, fill="both")
                frame.initial_tables_request()
                continue

            # Anything other than the controller is omitted.
            if frame.name != frame_name:
                frame.pack_forget()
                continue

            # Placing the controller on the left.
            frame.pack(side="left", expand=True, fill="both")
            frame.initial_info_request()

    # ------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------

# CUSTOMIZATIONS TO HOLD VALUES.


class CustomFrame(tb.Frame):
    """
    General class for the frames, inherited from tk.Frame to add some characteristics
    required by other classes, such as the name and the frame_handler asigned by the
    main window.
    """

    def __init__(self, root: tb.Window, name: str, frame_handler: FrameHandler):
        tb.Frame.__init__(self, root)
        self.frame_handler = frame_handler
        self.root = root
        self.name = name

    # ------------------------------------------------


class CustomEntry(tb.Entry):
    """
    General class for the entries, inherited from tb.Entry to add some characteristics
    required bu other classes, such as the row and column of the Entry and the type of
    details that it will be used for.
    """

    def __init__(self, frame: tb.Frame, row: int, col: int, entry_type: str):
        tb.Entry.__init__(self, frame)
        self.row = row
        self.col = col
        self.entry_type = entry_type

    # ------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class MainMenuFrame(CustomFrame):
    """
    First frame that is loaded that redirects to the other available options
    for configurations and working setups.
    """

    def __init__(self, root: tb.Window, frame_handler: FrameHandler):
        CustomFrame.__init__(self, root, "main_frame", frame_handler)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        self.serial_configuration_button = tb.Button(
            self,
            text="Serial Configuration",
            command=lambda: frame_handler.frame_packer("serial_configuration_frame"),
            padding=(5, 15),
            width=30,
            bootstyle="info",
        )

        self.robotic_configuration_button = tb.Button(
            self,
            text="Robotic Configuration",
            command=lambda: frame_handler.frame_packer("robotic_configuration_frame"),
            padding=(5, 15),
            width=30,
            bootstyle="info",
        )

        self.direct_kinematics_frame_button = tb.Button(
            self,
            text="Direct Kinematics",
            command=lambda: frame_handler.direct_kinematic_frame_packer(
                "direct_kinematics_frame"
            ),
            padding=(5, 15),
            width=30,
            bootstyle="success",
        )

        self.inverse_kinematics_frame_button = tb.Button(
            self,
            text="Inverse Kinematics",
            command=lambda: None,
            padding=(5, 15),
            width=30,
            bootstyle="dark",
            state="disabled",  # TODO: Not available yet.
        )

        self.guided_programming_frame_button = tb.Button(
            self,
            text="Guided Programming Sample",
            command=lambda: None,
            padding=(5, 15),
            width=30,
            bootstyle="dark",
            state="disabled",  # TODO: Not available yet.
        )

        self.exit_window_button = tb.Button(
            self,
            text="Exit",
            command=self.root.destroy,
            width=20,
            padding=(5, 10),
            bootstyle="danger",
        )

        # Main frame components placing.
        self.serial_configuration_button.place(relx=0.5, rely=0.2, anchor="center")
        self.robotic_configuration_button.place(relx=0.5, rely=0.3, anchor="center")
        self.direct_kinematics_frame_button.place(relx=0.5, rely=0.4, anchor="center")
        self.inverse_kinematics_frame_button.place(relx=0.5, rely=0.5, anchor="center")
        self.guided_programming_frame_button.place(relx=0.5, rely=0.6, anchor="center")
        self.exit_window_button.place(relx=0.5, rely=0.8, anchor="center")

    # ------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class SerialConfigurationFrame(CustomFrame):
    """
    Frame that has functionalities to make modifications to the Serial Communication, as well
    for loading some variables related to this.
    """

    def __init__(
        self,
        root: tb.Window,
        frame_handler: FrameHandler,
        serial_conn: SerialObject,
    ):
        CustomFrame.__init__(self, root, "serial_configuration_frame", frame_handler)

        # Serial object reference.
        self.serial_conn = serial_conn

        # Port data.
        self.available_ports_data = {}

        # Baudrate values reference.
        self.serial_baudrate_value = tb.StringVar(self.root)
        self.serial_baudrate_value.set(self.serial_conn.baudrate)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        self.load_serial_button = tb.Button(
            self, text="Load Ports", command=self.load_ports, width=20, padding=(5, 10)
        )

        self.combo_serial = tb.Combobox(self)

        self.combo_serial.bind("<<ComboboxSelected>>", self.update_label_serial_port)

        self.selected_port_name_label = tb.Label(self, text="NONE")

        self.selected_port_desc_label = tb.Label(self, text="...")

        self.baudrate_entry = tb.Entry(
            self,
            textvariable=self.serial_baudrate_value,
            validate="key",
            validatecommand=(self.root.register(self.number_validation), "%P"),
        )

        self.update_serial_configuration_button = tb.Button(
            self,
            text="Update",
            command=self.update_serial_configuration,
            width=20,
            padding=(5, 10),
        )

        self.home_return_button = tb.Button(
            self,
            text="Return",
            command=lambda: frame_handler.frame_packer("main_frame"),
            width=20,
            padding=(10, 20),
        )

        # Serial Configuration frame components placing.
        self.load_serial_button.place(relx=0.5, rely=0.2, anchor="center")
        self.selected_port_name_label.place(relx=0.5, rely=0.3, anchor="center")
        self.selected_port_desc_label.place(relx=0.5, rely=0.4, anchor="center")
        self.combo_serial.place(relx=0.5, rely=0.5, anchor="center")
        self.baudrate_entry.place(relx=0.5, rely=0.6, anchor="center")
        self.update_serial_configuration_button.place(
            relx=0.5, rely=0.7, anchor="center"
        )
        self.home_return_button.place(relx=0.5, rely=0.8, anchor="center")

        # Loading the available ports.
        self.load_ports()

        if self.serial_conn.port != None and len(self.available_ports_data) != 0:
            self.selected_port_name_label.configure(text=self.serial_conn.port)
            self.selected_port_desc_label.configure(
                text=self.available_ports_data[self.serial_conn.port]
            )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - Methods - - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def load_ports(self):
        """
        The function is used by a button who loads and refresh the
        current available port list in order for these to be selected
        in the combobox (combo_serial).
        """
        ports_data = self.serial_conn.get_ports()

        self.available_ports_data = {}

        for port, description, _ in ports_data:
            self.available_ports_data[port] = description

        listed_ports = list(self.available_ports_data.keys())

        self.combo_serial.configure(values=listed_ports)

    # ------------------------------------------------

    def update_label_serial_port(self, _):
        """
        This function updates the labels destinated to display the current selection
        for the serial configuration in regards to the port information exclusively.
        """
        # Extracting the information.
        selected_port = self.combo_serial.get()
        description = self.available_ports_data[selected_port]

        # Labels update.
        self.selected_port_name_label.configure(text=selected_port)
        self.selected_port_desc_label.configure(text=description)

    # ------------------------------------------------

    def update_serial_configuration(self):
        """
        Casting the value of the variable holding the baudrate from the entry
        to an integer and updating the configuration for the serial port.
        """
        # No baudrate specified.
        if self.baudrate_entry.get() == "":
            return
        # No port selected.
        if self.combo_serial.get() == None or self.combo_serial.get() == "":
            print("No changes")
            return

        self.serial_conn.port = self.combo_serial.get()
        self.serial_conn.baudrate = int(self.serial_baudrate_value.get())

        # Printing Serial details, remove if not required.
        print(f"PORT: {self.serial_conn.port} | BAUDRATE: {self.serial_conn.baudrate}")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # - - - - - - - - - - Bindings- - - - - - - - - - - - -
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def number_validation(self, new_value: str):
        """
        Callback function that is called when a new entry is set for the baudrate.
        This confirms if it is a number or a blank space in order to avoid chars in
        the value required as int.
        """
        if new_value.isdigit() or new_value == "":
            return True
        return False

    # ------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class RoboticConfigurationFrame(CustomFrame):
    """
    Frame that has functionalities to make modifications to the robotic parameters.
    Degrees or Radians visualization is available.
    """

    # TODO: Possible integration of end effector offset entries.
    def __init__(
        self,
        root: tb.Window,
        frame_handler: FrameHandler,
        robotic_properties: RoboticProperties,
    ):
        CustomFrame.__init__(self, root, "robotic_configuration_frame", frame_handler)

        # Saving the information of the robotic properties. Futher changes are also updated.
        self.robotic_properties = robotic_properties

        # Table lists to be able to clean the screen by deleting these objects.
        self.entries_parameters_table: List[List[CustomEntry]] = []
        self.button_actuator_table: List[tb.Button] = []
        self.entries_ranges_table: List[List[CustomEntry]] = []

        # Placing variables.
        self.start_x = 0.3
        self.start_y = 0.3
        self.step_x = 0.05
        self.step_y = 0.1

        # Visualization of degrees or radians.
        self.degrees_state = tb.BooleanVar()

        # - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        self.DOF_entry = tb.Spinbox(
            self,
            from_=self.robotic_properties.dof_inf_limit,
            to=self.robotic_properties.dof_upp_limit,
        )
        self.DOF_entry.set(self.robotic_properties.degrees_of_freedom)
        self.DOF_entry.bind("<Key>", self.block_keys)
        self.DOF_entry.bind("<<Increment>>", self.dof_modify_increase)
        self.DOF_entry.bind("<<Decrement>>", self.dof_modify_decrease)

        self.degrees_Checkbutton = tb.Checkbutton(
            self,
            text="Degrees",
            command=self.degrees_toggle_checkbutton,
            variable=self.degrees_state,
        )

        self.home_return_button = tb.Button(
            self,
            text="Return",
            command=lambda: frame_handler.frame_packer("main_frame"),
            width=20,
            padding=(10, 20),
        )

        # Placing components.
        self.DOF_entry.place(relx=0.3, rely=0.1, anchor="center")
        self.degrees_Checkbutton.place(relx=0.4, rely=0.1, anchor="center")
        self.home_return_button.place(relx=0.8, rely=0.5, anchor="center")

        # Placing the headings for the DH table.
        headings = ["θ", "d", "a", "α"]
        for col, head in enumerate(headings):
            label = tb.Label(self, text=head, justify="right")
            label.place(
                relx=self.start_x + col * self.step_x + 0.02,
                rely=self.start_y - self.step_y,
                anchor="center",
                width=80,
            )

        # Placing the heading for the Ranges.
        label = tb.Label(self, text="Ranges", justify="center")
        label.place(
            relx=self.start_x - self.step_x * 3.5,
            rely=self.start_y - self.step_y,
            anchor="center",
            width=50,
        )

        # Initial methods.
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
        """
        Initial request to create the entries from the table designed for the ranges.
        """
        # Looping rows.
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            new_row = []
            # Looping columns.
            for col in range(2):
                entry = self.create_entry_component(row, col, "RANGE")
                new_row.append(entry)

            # Adding to the table.
            self.entries_ranges_table.append(new_row)

    # ------------------------------------------------

    def initial_parameters_entries_request(self):
        """
        Initial request to create the entries from the table designed for the parameters.
        """
        # Looping rows.
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            new_row = []
            # Looping columns.
            for col in range(4):
                entry = self.create_entry_component(row, col, "PARAMETER")
                new_row.append(entry)

            # Adding to the table.
            self.entries_parameters_table.append(new_row)

    # ------------------------------------------------

    def initial_pointer_buttons_request(self):
        """
        Initial request to create the entries from the table designed for the buttons.
        """
        # Looping the vector.
        for row in range(0, self.robotic_properties.degrees_of_freedom):
            button = self.create_button_component(row)

            # Adding to the list.
            self.button_actuator_table.append(button)

    # ------------------------------------------------

    def block_keys(self, _):
        """
        Event that triggers when any key is tried to be introduced.
        Fully blocked functionality.
        """
        return "break"

    # ------------------------------------------------

    def create_entry_component(self, row: int, col: int, type_request: str):
        """
        Request to create an entry. Row and column information is passed as a parameter in order to
        update the information from the tables. Depending on the type request, the entry is created
        with certain characteristics.
        """

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
            entry.bind(
                "<FocusOut>",
                lambda event, row=row, col=col: self.entry_ranges_focus_out(
                    event, entry, row, col
                ),
            )
            value = self.robotic_properties.ranges[row, col]

        # Additional configuration for parameters entries.
        if type_request == "PARAMETER":
            idx = self.start_x + col * self.step_x
            entry.bind(
                "<FocusOut>",
                lambda event, row=row, col=col: self.entry_params_focus_out(
                    event, entry, row, col
                ),
            )
            value = self.robotic_properties.dh_params[row, col]

            # Styling in case it is the entry for a configurated actuator.
            if col == self.robotic_properties.pointer_actuators[row]:
                entry.configure(style="dh_params_config.TEntry")

        # Placing and inserting the value.
        entry.place(relx=idx, rely=idy, anchor="center", width=40)
        entry.insert(0, value)

        # Returning to be appended to the list.
        return entry

    # ------------------------------------------------

    def create_button_component(self, row: int):
        """
        Request to create the button to toggle the actuator type. The row details is passed to
        locate the object in the vector list and modify any required detail.
        """
        # Button creation and initial configuration.
        button = tb.Button(self)
        button.configure(command=partial(self.actuator_toggle_button, button, row))
        button.place(
            relx=self.start_x + 5 * self.step_x,
            rely=self.start_y + row * self.step_y,
            anchor="center",
            width=80,
        )

        # Text configuration according to the current settings for the actuators.
        button.configure(
            text=(
                "Linear"
                if self.robotic_properties.pointer_actuators[row]
                else "Rotatory"
            )
        )

        # Return button to be appended.
        return button

    # -----------------------------
    # @@@ Increase/Decrease DOF @@@
    # -----------------------------

    def dof_modify_increase(self, _: tk.Event):
        """
        Request to increase the degrees of freedom from the configuration. The Superior
        Limit can not be passed. Elements from the tables are modified, adding them to both
        the configuration and the visuals of the table.
        """
        # Verifying not passing the upper limit.
        if int(self.DOF_entry.get()) == self.robotic_properties.dof_upp_limit:
            return

        # Degrees of freedom increase, setting the row index.
        self.robotic_properties.degrees_of_freedom += 1
        row = self.robotic_properties.degrees_of_freedom - 1

        # Adding the new empty row for the DH parameters.
        new_line = np.array([0, 0, 0, 0])
        self.robotic_properties.dh_params = np.append(
            self.robotic_properties.dh_params, [new_line], axis=0
        )

        # Adding the new empty row for the ranges.
        new_line = np.array([0, 0])
        self.robotic_properties.ranges = np.append(
            self.robotic_properties.ranges, [new_line], axis=0
        )

        # Adding another pointer to the vector.
        self.robotic_properties.pointer_actuators = np.append(
            self.robotic_properties.pointer_actuators, 0
        )

        # Add a new line to the table, add visual entries. (RANGES, PARAMS Y BUTTON)
        new_row_ranges = []
        new_row_params = []

        # Ranges entries creation.
        for col in range(2):
            entry = self.create_entry_component(row, col, "RANGE")
            new_row_ranges.append(entry)

        # Params entries creation.
        for col in range(4):
            entry = self.create_entry_component(row, col, "PARAMETER")
            new_row_params.append(entry)

        # Button creation.
        button = self.create_button_component(row)

        # Adding to the list.
        self.entries_ranges_table.append(new_row_ranges)
        self.entries_parameters_table.append(new_row_params)
        self.button_actuator_table.append(button)

    # ------------------------------------------------

    def dof_modify_decrease(self, _: tk.Event):
        """
        Request to decrease the degrees of freedom from the configuration. The Inferior
        Limit can not be passed. Elements from the tables are modified, removing the last line
        from both the visual tables and the configuration.
        """
        # Verifying not passing the inferior limit.
        if int(self.DOF_entry.get()) == self.robotic_properties.dof_inf_limit:
            return

        # Decreasing the DOF, saving the index for the last row.
        self.robotic_properties.degrees_of_freedom -= 1
        previous_last_row = self.robotic_properties.degrees_of_freedom

        # Removing last row for the DH parameters.
        self.robotic_properties.dh_params = np.delete(
            self.robotic_properties.dh_params, previous_last_row, axis=0
        )

        # Removing last row for the ranges.
        self.robotic_properties.ranges = np.delete(
            self.robotic_properties.ranges,
            self.robotic_properties.degrees_of_freedom,
            axis=0,
        )

        # Removing the last pointer from the vector.
        self.robotic_properties.pointer_actuators = np.delete(
            self.robotic_properties.pointer_actuators, previous_last_row
        )

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

    def actuator_toggle_button(self, button: tb.Button, row: int):
        """
        This method changes the current state of the vector that determinates the parameter
        assigned for the actuator (Rotatory or linear). The color style is also changed, and the
        entries affected (Both ranges and parameter) are reset to zero.
        """
        # Getting the index for the current parameter of the actuator configuration.
        current_value = self.robotic_properties.pointer_actuators[row]

        # Toggle the variable with boolean logic and back to int.
        self.robotic_properties.pointer_actuators[row] = int(not (current_value))

        # Text configuration according to the current settings for the actuators.
        button.configure(
            text=(
                "Linear"
                if self.robotic_properties.pointer_actuators[row]
                else "Rotatory"
            )
        )

        # Calling method to reset entries.
        self.toggle_reset_entries(row)

    # ------------------------------------------------

    def toggle_reset_entries(self, row: int):
        """
        Resetting the affected entries back to zero in order to establish the new details
        of the ranges and parameter value manually.
        """
        # Pointer for the new parameter set as the actuator.
        pointer = int(self.robotic_properties.pointer_actuators[row])

        # Reset to the inferior range.
        self.entries_ranges_table[row][0].delete(0, tb.END)
        self.entries_ranges_table[row][0].insert(0, "0.0")
        self.robotic_properties.ranges[row, 0] = 0

        # Reset to the upper range.
        self.entries_ranges_table[row][1].delete(0, tb.END)
        self.entries_ranges_table[row][1].insert(0, "0.0")
        self.robotic_properties.ranges[row, 1] = 0

        # Reset of the new assigned parameter. Changing styles as well.
        self.entries_parameters_table[row][pointer].delete(0, tb.END)
        self.entries_parameters_table[row][pointer].insert(0, "0.0")
        self.entries_parameters_table[row][pointer].configure(
            style="dh_params_config.TEntry"
        )
        self.entries_parameters_table[row][int(not pointer)].configure(
            style="default.TEntry"
        )
        self.robotic_properties.dh_params[row, pointer] = 0

        # The default configuration is calculated.
        self.robotic_properties.default_configuration_request()

    # ------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@
    # @@@ Entry Validation @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@

    def entry_validation(self, value: str, _: str):
        """
        Validation of a proper entry inserted in the cells. Numbers are only accepted, as well for
        having an empty entry and the minus sign at the start of the number to represent negative values.
        """

        # Individual conditions. Anything outside these will not be accepted.
        if value == "" or value.replace(".", "", 1).isdigit():
            return True
        elif value == "-":
            return True
        elif value.replace(".", "", 1).isdigit() or (
            value.startswith("-") and value[1:].replace(".", "", 1).isdigit()
        ):
            return True
        else:
            return False

    # ------------------------------------------------

    def entry_ranges_focus_out(
        self, _: tk.Event, entry: CustomEntry, row: int, col: int
    ):
        """
        Function callback used when the entry for the ranges is out of focus, meaning that no more changes
        will be performed. The verification makes sure that ranges are taken in consideration, as well for
        leaving a numeric representation inside the cell.
        """
        # Extracting the current range limits.
        max_range = self.robotic_properties.ranges[row, 1]
        min_range = self.robotic_properties.ranges[row, 0]

        # Entry value.
        value = entry.get()

        # Index for the row affected. The value for the entry of the parameter is also extracted.
        param_actuator_affected = int(self.robotic_properties.pointer_actuators[row])
        value_parameter = self.robotic_properties.dh_params[
            row, param_actuator_affected
        ]

        # Empty condition.
        if value == "":
            value = 0
            entry.insert(0, "0.0")

        # Only minus condition.
        elif value == "-":
            value = 0
            entry.delete(0, tb.END)
            entry.insert(0, "0.0")

        # Numeric value validations.
        value = float(value)

        # Degrees mode ON.
        if self.degrees_state.get() and param_actuator_affected == 0:
            value = np.deg2rad(value)

        # Max limit passed verification.
        if col == 0 and value > max_range:
            value = max_range - 1
            entry.delete(0, tb.END)
            if self.degrees_state.get():
                entry.insert(0, np.rad2deg(value))
            else:
                entry.insert(0, value)

        # Min limit verification.
        elif col == 1 and value < min_range:
            value = min_range + 1
            entry.delete(0, tb.END)
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
            entry_parameter = self.entries_parameters_table[row][
                param_actuator_affected
            ]
            entry_parameter.delete(0, tb.END)
            if self.degrees_state.get():
                entry_parameter.insert(0, np.rad2deg(value_parameter))
            else:
                entry_parameter.insert(0, value_parameter)

            # The default configuration is calculated.
        self.robotic_properties.default_configuration_request()

    # ------------------------------------------------

    def entry_params_focus_out(
        self, _: tk.Event, entry: CustomEntry, row: int, col: int
    ):
        """
        Function callback used when the entry for the params is out of focus, meaning that no more changes
        will be performed. The verification makes sure that ranges are taken in consideration, as well for
        leaving a numeric representation inside the cell.
        """
        # Entry value.
        value = entry.get()

        # Extracting the current range limits.
        max_range = self.robotic_properties.ranges[row, 1]
        min_range = self.robotic_properties.ranges[row, 0]

        # Empty condition.
        if value == "":
            value = 0
            entry.insert(0, "0.0")

        # Only minus condition.
        elif value == "-":
            value = 0
            entry.delete(0, tb.END)
            entry.insert(0, "0.0")

        # Numeric value validations.
        value = float(value)

        # Degrees mode ON.
        if self.degrees_state.get() and (col == 0 or col == 3):
            value = np.deg2rad(value)

        # Max limit passed verification.
        if col == 0 and value > max_range:
            value = max_range
            entry.delete(0, tb.END)
            if self.degrees_state.get():
                entry.insert(0, np.rad2deg(value))
            else:
                entry.insert(0, value)

        # Min limit passed verification.
        elif col == 0 and value < min_range:
            value = min_range
            entry.delete(0, tb.END)
            if self.degrees_state.get():
                entry.insert(0, np.rad2deg(value))
            else:
                entry.insert(0, value)

        # Updating configuration for robot.
        self.robotic_properties.dh_params[row][col] = value

        # The default configuration is calculated.
        self.robotic_properties.default_configuration_request()

    # ------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@ Degrees/Radians Mode @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def degrees_toggle_checkbutton(self):
        """
        Function that calls the corresponding methods to perform the modification of
        the available cells from degrees to radians or backwards.
        """
        self.toggle_angles_ranges()
        self.toggle_angles_params()

    # ------------------------------------------------

    def toggle_angles_ranges(self):
        """
        Method to check each of the rows and, in case the configuration states it, the
        visual table for the ranges is updated to degrees or radians mode, depending
        on the state of the checkbutton.
        """
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
            inf_range_entry.delete(0, tb.END)
            inf_range_entry.insert(0, value_inf_range)

            # Updating superior limit entry.
            sup_range_entry.delete(0, tb.END)
            sup_range_entry.insert(0, value_sup_range)

    # ------------------------------------------------

    def toggle_angles_params(self):
        """
        Method to check each of the rows and, in case the configuration states it, the
        visual table for the parameters is updated to degrees or radians mode, depending
        on the state of the checkbutton.
        """
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
            theta_entry.delete(0, tb.END)
            theta_entry.insert(0, value_theta)

            # Updating alpha entry.
            alpha_entry.delete(0, tb.END)
            alpha_entry.insert(0, value_alpha)

    # ------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class RoboticParamsFrame(CustomFrame):
    """
    Frame to visualize the Robotic Parameters in the Direct Kinematics mode.
    On each update for the commands being sent to the robot the visual tables
    are also modified.
    """

    def __init__(
        self,
        root: tb.Window,
        frame_handler: FrameHandler,
        robotic_properties: RoboticProperties,
    ):
        CustomFrame.__init__(self, root, "robotic_params_frame", frame_handler)

        # Shared robotic properties by all classes.
        self.robotic_properties = robotic_properties

        # - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        # DH PARAMETERS TABLE.
        self.dh_parameters_label = tb.Label(self, text="DH Parameters")

        self.dh_parameters_table = tb.Treeview(
            self,
            columns=("theta", "d", "a", "alpha"),
            show="headings",
            height=self.robotic_properties.degrees_of_freedom,
        )

        self.dh_parameters_table.heading("theta", text="θ")
        self.dh_parameters_table.column(
            "theta", minwidth=100, width=100, stretch=tk.NO, anchor=tk.CENTER
        )

        self.dh_parameters_table.heading("d", text="d")
        self.dh_parameters_table.column(
            "d", minwidth=100, width=100, stretch=tk.NO, anchor=tk.CENTER
        )

        self.dh_parameters_table.heading("a", text="a")
        self.dh_parameters_table.column(
            "a", minwidth=100, width=100, stretch=tk.NO, anchor=tk.CENTER
        )

        self.dh_parameters_table.heading("alpha", text="α")
        self.dh_parameters_table.column(
            "alpha", minwidth=100, width=100, stretch=tk.NO, anchor=tk.CENTER
        )

        # TRANSFORMATION MATRIX TABLE.
        self.transformation_matrix_label = tb.Label(self, text="Transformation Matrix")

        self.transformation_matrix_table = tb.Treeview(
            self, columns=("A", "B", "C", "D"), show="tree", height=4
        )
        self.transformation_matrix_table.column("#0", width=0)
        self.transformation_matrix_table.column(
            "A", minwidth=0, width=100, anchor=tk.CENTER
        )
        self.transformation_matrix_table.column(
            "B", minwidth=0, width=100, anchor=tk.CENTER
        )
        self.transformation_matrix_table.column(
            "C", minwidth=0, width=100, anchor=tk.CENTER
        )
        self.transformation_matrix_table.column(
            "D", minwidth=0, width=100, anchor=tk.CENTER
        )

        # END EFFECTOR TABLE.
        self.final_efector_position_label = tb.Label(
            self, text="Final Efector Position", background="green"
        )

        self.final_efector_position_table = tb.Treeview(
            self, columns=("X", "Y", "Z"), show="headings", height=1
        )
        self.final_efector_position_table.heading("X", text="X")
        self.final_efector_position_table.column(
            "X", minwidth=0, width=100, anchor=tk.CENTER
        )

        self.final_efector_position_table.heading("Y", text="Y")
        self.final_efector_position_table.column(
            "Y", minwidth=0, width=100, anchor=tk.CENTER
        )

        self.final_efector_position_table.heading("Z", text="Z")
        self.final_efector_position_table.column(
            "Z", minwidth=0, width=100, anchor=tk.CENTER
        )

        # Placing components.
        self.dh_parameters_label.place(relx=0.5, rely=0.1, anchor="center")
        self.dh_parameters_table.place(relx=0.5, rely=0.25, anchor="center")

        self.transformation_matrix_label.place(relx=0.5, rely=0.5, anchor="center")
        self.transformation_matrix_table.place(relx=0.5, rely=0.6, anchor="center")

        self.final_efector_position_label.place(relx=0.5, rely=0.7, anchor="center")
        self.final_efector_position_table.place(relx=0.5, rely=0.8, anchor="center")

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # MAIN FUNCTIONS.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

    def initial_tables_request(self):
        """
        Initial display of tables at the starting of the frame. The robotic properties
        are also updated (Setting the default configuration). This method is only called once.
        """
        # Reset the DH active table to the save table. Action performed on both initial requests.
        self.robotic_properties.default_configuration_request()

        # Resize according to the set DOF size.
        self.dh_parameters_table.configure(
            height=self.robotic_properties.degrees_of_freedom
        )

        # Updating the available tables.
        self.update_all_tables(False)

    # ------------------------------------------------

    def individual_table_update(
        self,
        num_table: np.ndarray,
        visual_table: ttk.Treeview,
        degrees_mode_state: bool,
    ):
        """
        Function to update one of the three available tables in the screen. The given table
        (Numeric Table) is from where the information will be taken, the visual table is the
        one to be updated. The boolean parameter sets the visuals for the first column and last
        columns in degrees or radians.
        """
        # Taking each element of the table and applying the delete function.
        visual_table.delete(*visual_table.get_children())

        # Iterating items of the numeric table.
        for row, items in enumerate(num_table):
            # In case the table is the end effector vector, appending as a simple list and exiting.
            if visual_table == self.final_efector_position_table:
                rounded_items = np.around(num_table, decimals=3)
                visual_table.insert("", tk.END, values=list(rounded_items))
                break

            # If the table is the DH params or the transformation matrix, performing updates.
            rounded_items = np.around(items, decimals=3)

            # If degrees visualization, affecting only the DH params table.
            if degrees_mode_state and visual_table == self.dh_parameters_table:
                rounded_items[0] = np.rad2deg(items[0])
                rounded_items[0] = np.around(rounded_items[0], decimals=3)
                rounded_items[3] = np.rad2deg(items[3])
                rounded_items[3] = np.around(rounded_items[3], decimals=3)

            visual_table.insert("", tk.END, iid=row, values=list(rounded_items))

    # ------------------------------------------------

    def update_all_tables(self, degrees_mode_state: bool):
        """
        Request to update all the tables in scene (Direct Kinematics details). These are
        the DH parameters, transformation matrix and final effector position. The update also
        takes the modifications of the parameters in consideration.
        """
        # DH parameters.
        self.individual_table_update(
            self.robotic_properties.dh_params_active_table,
            self.dh_parameters_table,
            degrees_mode_state,
        )
        # Transformation matrix.
        self.individual_table_update(
            self.robotic_properties.final_transformation_matrix,
            self.transformation_matrix_table,
            degrees_mode_state,
        )
        # End effector position.
        self.individual_table_update(
            self.robotic_properties.final_efector_vector,
            self.final_efector_position_table,
            degrees_mode_state,
        )


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class DirectKinematicsFrame(CustomFrame):
    """
    Frame to handle the request of the Direct Kinematics controller. Different buttons and
    checkbuttons are set, as well for the scales according to the DoF and settings for each of
    the actuators that can be controlled.
    """

    def __init__(
        self,
        root: tb.Window,
        frame_handler: FrameHandler,
        robotic_properties: RoboticProperties,
        robotic_params_frame: RoboticParamsFrame,
        serial_conn: SerialObject,
    ):
        CustomFrame.__init__(self, root, "direct_kinematics_frame", frame_handler)

        # Serial Configuration Object shared by some frames.
        self.serial_conn = serial_conn

        # Robotic properties shared by all frames.
        self.robotic_properties = robotic_properties
        self.robotic_params_frame = robotic_params_frame

        # Variable to hold the state of the checkbuttons.
        self.continous_mode_state = tb.BooleanVar()
        self.continous_mode_state.set(False)
        self.degrees_mode_state = tb.BooleanVar()
        self.degrees_mode_state.set(False)

        # Storage for scales for controllers of each actuator.
        self.scales_table: List[tb.Scale] = []
        self.title_labels_table: List[tb.Label] = []
        self.value_labels_table: List[tb.Label] = []

        # Placing index variables.
        self.start_x = 0.5
        self.separation_x = 0.2
        self.start_y = 0.3
        self.step_y = 0.1

        # - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        self.continous_mode_checkbutton = tb.Checkbutton(
            self,
            text="Auto Mode",
            command=self.continous_mode_toggle,
            variable=self.continous_mode_state,
        )

        self.degrees_mode_checkbutton = tb.Checkbutton(
            self,
            text="Degrees Mode",
            command=self.degrees_mode_toggle,
            variable=self.degrees_mode_state,
        )

        # TODO: Possible integration of progressbar or Floodgauge to check status of message.
        # In order to avoid sending multiple instructions.
        self.send_command_button = tb.Button(
            self,
            text="Send Command",
            command=self.send_multiple_command_request,
            bootstyle="success",
        )

        self.default_position_button = tb.Button(
            self,
            text="Default Position",
            command=self.default_position_request,
            bootstyle="info",
        )

        self.home_return_button = tb.Button(
            self,
            text="Return",
            command=lambda: frame_handler.frame_packer("main_frame"),
            width=20,
            padding=(10, 20),
            bootstyle="dark",
        )

        # Placing components.
        self.continous_mode_checkbutton.place(
            relx=0.5,
            rely=0.10,
            anchor="center",
        )
        self.degrees_mode_checkbutton.place(
            relx=0.5,
            rely=0.20,
            anchor="center",
        )
        self.default_position_button.place(
            relx=0.85,
            rely=0.1,
            anchor="center",
            width=150,
            height=50,
        )
        self.home_return_button.place(
            relx=0.85,
            rely=0.2,
            anchor="center",
            width=150,
            height=50,
        )
        self.send_command_button.place(
            relx=0.15,
            rely=0.15,
            anchor="center",
            width=150,
            height=50,
        )

    # - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # MAIN FUNCTIONS.
    # - - - - - - - - - - - - - - - - - - - - - - - - - - -

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@        General        @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def initial_info_request(self):
        """
        Sets the default configuration for the robot, clears the available
        scales if any, and creates and appends the scales and labels for the
        actuators according to the degrees of freedom and the current
        configuration for these actuators.
        """

        # Reset to the default configuration of the robot.
        self.robotic_properties.default_configuration_request()

        # Clearing the list, in case it was previously used.
        for scale in self.scales_table:
            scale.destroy()
        for title_label in self.title_labels_table:
            title_label.destroy()
        for title_label in self.value_labels_table:
            title_label.destroy()

        self.scales_table = []
        self.title_labels_table = []
        self.value_labels_table = []

        # Gathering the available degrees of freedom.
        degrees_of_freedom = self.robotic_properties.degrees_of_freedom

        # Creating individual scales for each actuator.
        for row in range(degrees_of_freedom):
            scale, value_label = self.create_scale_component(row)
            title_label = self.create_label_component(row)

            self.scales_table.append(scale)
            self.value_labels_table.append(value_label)
            self.title_labels_table.append(title_label)

    # ------------------------------------------------

    def create_scale_component(self, row: int):
        """
        Individual creation of the scale for each of the degrees of freedom
        of the system. The row is also attached to establish the position
        in the window, as well for the label assignments.
        """
        # Positional variables.
        idx = self.start_x + self.separation_x
        idy = self.start_y + row * self.step_y

        # Pointer values extraction.
        actuator_pointer = int(self.robotic_properties.pointer_actuators[row])
        default_value = self.robotic_properties.dh_params[row, actuator_pointer]
        min_range = self.robotic_properties.ranges[row, 0]
        max_range = self.robotic_properties.ranges[row, 1]

        # Creation of individual scale component.
        scale = ttk.Scale(
            self,
            from_=min_range,
            to=max_range,
            orient=tk.HORIZONTAL,
            length=300,
            value=default_value,
        )

        # Creation of the corresponding label for the value.
        label = ttk.Label(self)
        label.configure(text=f"{float(default_value):.4f}")
        if self.degrees_mode_state.get():
            label.config(text=f"{np.rad2deg(float(default_value)):.4f}")

        # Placing both components.
        scale.place(relx=idx, rely=idy, anchor=tb.CENTER)
        label.place(relx=idx - 2 * self.separation_x, rely=idy, anchor=tb.CENTER)

        # Once created, the label is also attached as a parameter for the method.
        scale.configure(
            command=lambda value, label=label, row=row: self.scale_updates(
                value, label, row
            )
        )

        # Returning to be appended to the list.
        return scale, label

    # ------------------------------------------------

    def create_label_component(self, row: int):
        """
        Individual label creation for the actuator title. The row is sent to
        indicate the actuator being affected (Starting from 1).
        """
        # Positional variables.
        idx = self.start_x - 2 * self.separation_x
        idy = self.start_y + row * self.step_y

        # Title.
        title = f"Actuator {row + 1}"

        # Label configuration.
        label = tb.Label(self, text=title)
        label.place(relx=idx, rely=idy, anchor=tb.CENTER)

        # Returning to be appended.
        return label

    # ------------------------------------------------

    def degree_labeling(self, label: tk.Label, value: str):
        """
        Function called when the toggle for the degrees mode is set or called from
        other functions to check the specific visualization required (Deg or Rad).
        """
        # Checking with is the current mode.
        if self.degrees_mode_state.get():
            label.configure(text=f"{np.rad2deg(float(value)):.4f}")
        else:
            label.config(text=f"{float(value):.4f}")

    # ------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@       Requests        @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def continous_mode_toggle(self):
        """
        Condition to check the current mode of the system in order to send the command
        when passing from OFF to ON, to update the values to the current configuration
        of the scales.
        """
        self.degrees_mode_toggle()

        # Only when entering the continous mode the current settings are sent.
        if self.continous_mode_state.get():
            self.send_multiple_command_request()

    # ------------------------------------------------

    def degrees_mode_toggle(self):
        """
        When toggle or called, the labeling is updated according to the current state
        of the checkbutton. Information is presented as Degrees or Radians.
        """
        for row, label in enumerate(self.value_labels_table):
            scale = self.scales_table[row]
            value = scale.get()

            self.degree_labeling(label, value)

        self.robotic_params_frame.update_all_tables(self.degrees_mode_state.get())

    # ------------------------------------------------

    def default_position_request(self):
        """
        Action to set the default configuration of the robot both in the parameters and
        the visual tables. An instruction is also sent to the robot to set the starting
        position (Either when the DK Frame is starting or as per user request).
        """
        for row, scale in enumerate(self.scales_table):
            # Setting the pointer values.
            actuator_pointer = int(self.robotic_properties.pointer_actuators[row])
            default_value = self.robotic_properties.dh_params[row, actuator_pointer]

            # Extracting the corresponding label for the value display.
            value_label = self.value_labels_table[row]

            # Setting the values back to the default configuration.
            scale.set(default_value)
            self.degree_labeling(value_label, default_value)

        # Set the tables also to the default position.
        self.robotic_properties.default_configuration_request()
        self.robotic_params_frame.update_all_tables(self.degrees_mode_state.get())

        # Sending the default configuration signal to the robot.
        self.send_multiple_command_request()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@     Scale Update      @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def scale_updates(self, value: str, label: ttk.Label, row: int):
        """
        Individual update of the scale binded to each of them. The label is
        always updated on change. The degrees or radian configuration is also
        checked to update the information as well.
        """

        # Updating text always.
        self.degree_labeling(label, value)

        # Send command if the mode is available.
        if self.continous_mode_state.get():
            self.individual_command_request(value, row)

    # ------------------------------------------------

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # @@@        Sending        @@@
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    def individual_command_request(self, value: str, row: int):
        """
        Method to send an individual command over the serial communication. This
        functions is used by the continous mode to send the changes to individual scales
        over the robot.
        """
        # Variable to store serial data.
        short_value = np.around(float(value), 3)
        command = f'I#Q{row}:{short_value};'

        print(command)
        # Attempting to send serial data.
        try:
            self.serial_conn.write(command.encode())
        except:
            print("UNABLE TO SEND")

        # Updating the information in the tables, as well for the visualizations.
        self.robotic_properties.update_dh_table_request(float(value), row)
        self.robotic_properties.update_matrices_request()
        self.robotic_params_frame.update_all_tables(self.degrees_mode_state.get())

    # ------------------------------------------------

    def send_multiple_command_request(self):
        """
        Method to send the information from all the scales when called. Is used when setting
        the default configuration and when the user request it not in the Continous Mode.
        """
        # Starting command (Empty).
        command = "M#"

        # Updating information for the scales and DH parameters.
        for row, scale in enumerate(self.scales_table):
            value = scale.get()
            self.robotic_properties.update_dh_table_request(float(value), row)

            # Shorten value appended.
            short_value = np.around(float(value), 3)
            command+=f'Q{row}:{short_value};'

        print(command)
        print(self.serial_conn.is_open)
        # Attempting to send serial data.
        try:
            self.serial_conn.write(command.encode())
        except:
            print("UNABLE TO SEND")

        # Updating visual information.
        self.robotic_properties.update_matrices_request()
        self.robotic_params_frame.update_all_tables(self.degrees_mode_state.get())

# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class InverseKinematicsFrame(CustomFrame):
    """ """

    def __init__(
        self,
        root: tb.Window,
        frame_handler: FrameHandler,
        robotic_properties: RoboticProperties,
    ):
        CustomFrame.__init__(self, root, "inverse_kinematics_frame", frame_handler)

        self.robotic_properties = robotic_properties

        # - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        self.home_return_button = tb.Button(
            self,
            text="Return",
            command=lambda: frame_handler.frame_packer("main_frame"),
            width=20,
            padding=(10, 20),
        )

        # Packing components.
        self.home_return_button.place(relx=0.5, rely=0.8, anchor="center")


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------


class GuidedProgrammingFrame(CustomFrame):
    """ """

    def __init__(self, root: tb.Window, frame_handler: FrameHandler):
        CustomFrame.__init__(self, root, "guided_programming_frame", frame_handler)

        # - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # - - - - - - - - - - GUI Components- - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - -

        self.home_return_button = tb.Button(
            self,
            text="Return",
            command=lambda: frame_handler.frame_packer("main_frame"),
            width=20,
            padding=(10, 20),
        )

        # Packing components.
        self.home_return_button.place(relx=0.5, rely=0.8, anchor="center")


# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------------------
