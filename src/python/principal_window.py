import tkinter as tk
from frames_gui import *
from typing import List
from serial_library import SerialObject



# TODO: 
# Here define the window (Already done).

# First define the robot properties, then update the frames.

# Define the initial DH parameters and pass them as parameters.
# Define initial configurations for robotics_properties.
# Define initial configurations for serial_configuration.


class PrincipalWindow:
    def __init__(self, root:tk.Tk):
        # Reference to the main application.
        self.root = root

        # Reference for the Serial Object, for both configuration and connection.
        self.serial_conn = SerialObject()
        # self.serial_conn.establish_parameters('COM1', 9600)

        # Reference for the handler of the frames.
        self.frames_handler = FrameHandler()

        # Frames used in this application.
        self.main_menu_frame = MainMenuFrame(root, self.frames_handler)
        self.serial_menu_frame = SerialConfigurationFrame(root, self.frames_handler, self.serial_conn)
        self.robotic_configuration_frame = RoboticConfigurationFrame(root, self.frames_handler)
        self.direct_kinematics_frame = DirectKinematicsFrame(root, self.frames_handler)
        self.inverse_kinematics_frame = InverseKinematicsFrame(root, self.frames_handler)

        frames:List[tk.Frame] = [
            self.main_menu_frame,
            self.serial_menu_frame,
            self.robotic_configuration_frame,
            self.direct_kinematics_frame,
            self.inverse_kinematics_frame
            ]
        
        # Updating the frames container in the Handler. Calling the first frame.
        self.frames_handler.frames = frames
        self.frames_handler.frame_packer('main_frame')

    # -------------------------------------------------------------------------------    

    # -------------------------------------------------------------------------------    

if __name__ == '__main__':

    root = tk.Tk()
    root.title("Robot Serial Interface")
    root.geometry('1200x600')
    root.configure(background='#F0ECD2')
    
    principal_window = PrincipalWindow(root)

    root.mainloop()