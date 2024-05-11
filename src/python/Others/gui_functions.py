import tkinter as tk
from tkinter import ttk
from serial import Serial
import python.Others.serial_configuration as serial_configuration
from robotic_library import *
import numpy as np

class ControlGUI:
    '''
    Class with all the implementations for the current GUI design and methods used to communicate the controller
    with the robot. No specific Micro is required, it is only needed the considerations in the codes being sent 
    through the serial communication. The instance also establishes the configuration for the serial communication.
    '''

    def __init__(self, root: tk.Tk):
        # Root object for tkinter passed as a parameter.
        self.root = root

        # Serial variables and configuration.
        self.serial_conn = Serial(None, 9600, timeout=10)
        self.available_ports_data = {}

        # Other Variables.
        self.continous_mode_state = tk.IntVar()

        self.serial_baudrate_value = tk.StringVar(self.root)
        self.serial_baudrate_value.set("9600")

        # Frames created and used for the robot controller.
        self.main_frame = tk.Frame(self.root)
        self.serial_configuration_frame = tk.Frame(self.root)
        self.direct_kinematics_frame = tk.Frame(self.root, background='gray')
        self.robotic_details_frame = tk.Frame(self.root, background='#DAF0D2')

        # DH Parameters and Homogeneous Matrix variables.
        self.robotic_properties = RoboticProperties()

        # Style configurations.
        style = ttk.Style()
        style.configure('Treeview.Heading', foreground = '#581845', font = ('Calibri', 14,'bold'))

        self.label_title_style = ttk.Style()
        self.label_title_style.configure("tittle.label", background='blue', foreground='red')

        # /////////////////////////////////////////////////////////////////////
        #            SECTION: COMPONENTS INITIALIZATION AND PACKING.
        # ////////////////////////////////////////////////////////////////////

        # @ @ @ Main Frame components @ @ @

        self.serial_configuration_button = tk.Button(self.main_frame,
                                                     text="Serial Configuration",
                                                     command=lambda:self.frame_packer(self.serial_configuration_frame),
                                                     height=2,
                                                     width=20)
        
        self.direct_kinematics_frame_button = tk.Button(self.main_frame, 
                                                        text="Direct Kinematics", 
                                                        command=lambda:self.direct_kinematic_frame_packer(self.direct_kinematics_frame),
                                                        height=2, 
                                                        width=20)
        
        self.inverse_kinematics_frame_button = tk.Button(self.main_frame, 
                                                        text="Inverse Kinematics", 
                                                        command=self.toggle_continous_mode,
                                                        height=2, 
                                                        width=20)
        
        self.exit_window_button = tk.Button(self.main_frame, 
                                            text="Exit", 
                                            command=self.close_window,
                                            height=2, 
                                            width=20)

        # Main frame components placing.
        self.serial_configuration_button.place(relx=0.5, rely=0.3, anchor='center')
        self.direct_kinematics_frame_button.place(relx=0.5, rely=0.4, anchor='center')
        self.inverse_kinematics_frame_button.place(relx=0.5, rely=0.5, anchor='center')
        self.exit_window_button.place(relx=0.5, rely=0.7, anchor='center')

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
        self.load_serial_button.place(relx=0.5, rely=0.2, anchor='center')
        self.selected_port_name_label.place(relx=0.5, rely=0.3, anchor='center')
        self.selected_port_desc_label.place(relx=0.5, rely=0.4, anchor='center')
        self.combo_serial.place(relx=0.5, rely=0.5, anchor='center')
        self.baudrate_entry.place(relx=0.5, rely=0.6, anchor='center')
        self.update_serial_configuration_button.place(relx=0.5, rely=0.7, anchor='center')
        self.home_serial_configuration_button.place(relx=0.5, rely=0.8, anchor='center')

        # -------------------------------------------------------------------------------

        # TODO: Implement the continous mode.
        # FIXME: Implement the function to create the scales and store them in an array. This way, the program is not
        # limited to 3 DoF.

        # @ @ @ Commands Sender Frame components @ @ @

        self.continous_mode_checkbutton = tk.Checkbutton(self.direct_kinematics_frame, 
                                                         text='Auto',
                                                         command=None,
                                                         variable=self.continous_mode_state)

        self.q1_label = tk.Label(self.direct_kinematics_frame,
                                 text="Q1",
                                 )

        self.slide_q1 = tk.Scale(self.direct_kinematics_frame, 
                                from_=-90, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                #label='Q1',
                                width=20, length=300,
                                command=self.scale_changes)
        
        self.q2_label = tk.Label(self.direct_kinematics_frame,
                                 text="Q2",
                                 )
        
        self.slide_q2 = tk.Scale(self.direct_kinematics_frame, 
                                from_=0, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                #label='Q2', 
                                width=20, length=300,
                                command=self.scale_changes)
        
        self.q3_label = tk.Label(self.direct_kinematics_frame,
                                 text="Q3")
        
        self.slide_q3 = tk.Scale(self.direct_kinematics_frame, 
                                from_=0, 
                                to=90, 
                                orient=tk.HORIZONTAL, 
                                #label='Q3', 
                                width=20, length=300,
                                command=self.scale_changes)
        
        self.send_command_button = tk.Button(self.direct_kinematics_frame, 
                                     text="Send Command", 
                                     command=self.send_commands)

        self.home_button = tk.Button(self.direct_kinematics_frame, 
                                     text="Return", 
                                     command=lambda:self.frame_packer(self.main_frame))
        
        # Setting the default position.
        self.slide_q1.set(np.rad2deg(self.robotic_properties.q[0]))
        self.slide_q2.set(np.rad2deg(self.robotic_properties.q[1]))
        self.slide_q3.set(np.rad2deg(self.robotic_properties.q[2]))

        # Command sender frame packing.
        self.continous_mode_checkbutton.place(relx=0.7, rely=0.2, anchor='center')

        self.q1_label.place(relx=0.2, rely=0.3, anchor='center')
        self.slide_q1.place(relx=0.5, rely=0.3, anchor='center')

        self.q2_label.place(relx=0.2, rely=0.4, anchor='center')
        self.slide_q2.place(relx=0.5, rely=0.4, anchor='center')

        self.q3_label.place(relx=0.2, rely=0.5, anchor='center')
        self.slide_q3.place(relx=0.5, rely=0.5, anchor='center')

        self.send_command_button.place(relx=0.5, rely=0.6, anchor='center', width=250, height=50)
        self.home_button.place(relx=0.5, rely=0.8, anchor='center', width=200, height=50)

        # -------------------------------------------------------------------------------    

        # @ @ @ Robotics details components @ @ @

        self.dh_parameters_label = tk.Label(self.robotic_details_frame,
                                            text="DH Parameters")

        self.dh_parameters_table = ttk.Treeview(self.robotic_details_frame, columns=("theta", "d", "a", "alpha"), 
                                                show="headings", height=self.robotic_properties.degrees_of_freedom)

        self.dh_parameters_table.heading("theta", text="θ")
        self.dh_parameters_table.column("theta", minwidth=100, width=100, stretch=tk.NO, anchor=tk.CENTER)

        self.dh_parameters_table.heading("d", text="d")
        self.dh_parameters_table.column("d", minwidth=100, width=100, stretch=tk.NO, anchor=tk.CENTER)

        self.dh_parameters_table.heading("a", text="a")
        self.dh_parameters_table.column("a", minwidth=100, width=100, stretch=tk.NO, anchor=tk.CENTER)

        self.dh_parameters_table.heading("alpha", text="α")
        self.dh_parameters_table.column("alpha", minwidth=100, width=100, stretch=tk.NO, anchor=tk.CENTER)

        # - - - - 

        self.transformation_matrix_label = tk.Label(self.robotic_details_frame,
                                                    text="Transformation Matrix")

        self.transformation_matrix_table = ttk.Treeview(self.robotic_details_frame, columns=("A", "B", "C", "D"), show="tree", height=4)
        self.transformation_matrix_table.column("#0", width=0)
        self.transformation_matrix_table.column("A", minwidth=0, width=100, anchor=tk.CENTER)
        self.transformation_matrix_table.column("B", minwidth=0, width=100, anchor=tk.CENTER)
        self.transformation_matrix_table.column("C", minwidth=0, width=100, anchor=tk.CENTER)
        self.transformation_matrix_table.column("D", minwidth=0, width=100, anchor=tk.CENTER)

        # - - - - 

        self.final_efector_position_label = tk.Label(self.robotic_details_frame,
                                                    text="Final Efector Position",
                                                    background='green')

        self.final_efector_position_table = ttk.Treeview(self.robotic_details_frame, columns=("X", "Y", "Z"), show="headings", height=1)
        self.final_efector_position_table.heading("X", text="X")
        self.final_efector_position_table.column("X", minwidth=0, width=100, anchor=tk.CENTER)

        self.final_efector_position_table.heading("Y", text="Y")
        self.final_efector_position_table.column("Y", minwidth=0, width=100, anchor=tk.CENTER)

        self.final_efector_position_table.heading("Z", text="Z")
        self.final_efector_position_table.column("Z", minwidth=0, width=100, anchor=tk.CENTER)
        
        # Robotics details frame packing.
        self.dh_parameters_label.place(relx=0.5, rely=0.2, anchor='center')
        self.dh_parameters_table.place(relx=0.5, rely=0.3, anchor='center')

        self.transformation_matrix_label.place(relx=0.5, rely=0.4, anchor='center')
        self.transformation_matrix_table.place(relx=0.5, rely=0.5, anchor='center')

        self.final_efector_position_label.place(relx=0.5, rely=0.73, anchor='center')
        self.final_efector_position_table.place(relx=0.5, rely=0.8, anchor='center')

        self.update_table(self.robotic_properties.dh_params_save_table, self.dh_parameters_table)
        self.update_table(self.robotic_properties.final_transformation_matrix, self.transformation_matrix_table)
        self.update_table(self.robotic_properties.final_efector_vector, self.final_efector_position_table)

        # -------------------------------------------------------------------------------    

        # ----------------------------------
        # SECTION: FRAMES ORGANIZATION.
        # ----------------------------------

        self.frames = [
            self.main_frame,
            self.serial_configuration_frame,
            self.direct_kinematics_frame,
            self.robotic_details_frame
        ]

        # -------------------------------------------------------------------------------    

        # Methods used at the start of the App.
        self.frame_packer(self.main_frame)
        self.send_commands()


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
            frame.pack(expand=True, fill='both')
    
    # ------------------------------------------------------------------------

    def direct_kinematic_frame_packer(self, selected_frame:tk.Frame):
        '''
        
        '''
        for frame in self.frames:

            if frame == self.robotic_details_frame:
                frame.pack(side="right", anchor="center", expand=True, fill='both')
                continue

            if frame != selected_frame:
                frame.pack_forget()
                continue

            frame.pack(side="left", expand=True, fill='both')

    # ------------------------------------------------------------------------

    def close_window(self):
        '''
        
        '''
        self.root.destroy()

    # ------------------------------------------------------------------------

    def update_table(self, table:np.ndarray, visual_table:ttk.Treeview):
        '''

        '''
        
        # Taking each element of the table and applying the delete function.
        visual_table.delete(*visual_table.get_children())

        for count, row in enumerate(table):
            rounded_row = np.around(row, decimals=3)

            if visual_table == self.final_efector_position_table:

                # TODO: Remove this print.
                #print(self.robotic_properties.final_efector_vector)

                visual_table.insert("", tk.END, values=list(self.robotic_properties.final_efector_vector))
                break

            visual_table.insert("", "end", iid=count, values=list(rounded_row))

    # ------------------------------------------------------------------------

            
    # ----------------------------------
    # SECTION: SENDING COMMANDS OPTIONS.
    # ----------------------------------

    def scale_changes(self, value):
        if self.continous_mode_state.get():
            print(value)

    # ------------------------------------------------------------------------

    # FIXME: CHANGE THE LOCATION OF THIS FUNCTION.
    def toggle_continous_mode(self):
        print(self.continous_mode_state.get())

    # ------------------------------------------------------------------------
    
    def send_commands(self):
        # In case no port has been configurated the update can not be completed.
        if self.serial_conn.port == None:
            None
            #return # TODO: Commented for debbuging purposes.

        #FIXME: Possible in future iterations, make Q1 knobs variables in case more DoF are implemented.
        q1_value = self.slide_q1.get()
        q2_value = self.slide_q2.get()
        q3_value = self.slide_q3.get()

        command = f'M#Q1-{q1_value},Q2-{q2_value},Q3-{q3_value}'

        q1_rad_value = np.deg2rad(q1_value)
        q2_rad_value = np.deg2rad(q2_value)
        q3_rad_value = np.deg2rad(q3_value)

        #TODO: SEND TO SERIAL
        #TODO: Update the tables.

        #FIXME: Note that q is not always the variable, this could be later changed for linear actuators.
        self.robotic_properties.q[0] = q1_rad_value
        self.robotic_properties.q[1] = q2_rad_value
        self.robotic_properties.q[2] = q3_rad_value

        self.robotic_properties.initial_tables_creation()

        self.update_table(self.robotic_properties.dh_params_save_table, self.dh_parameters_table)
        self.update_table(self.robotic_properties.final_transformation_matrix, self.transformation_matrix_table)
        self.update_table(self.robotic_properties.final_efector_vector, self.final_efector_position_table)

    # oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo


if __name__ == '__main__':

    root = tk.Tk()
    root.title("Robot Serial Interface")
    root.geometry('1200x600')
    root.configure(background='#F0ECD2')
    control_gui = ControlGUI(root)

    root.mainloop()