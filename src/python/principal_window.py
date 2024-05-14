import ttkbootstrap as tb

from typing import List

from frames_library import *
from serial_library import SerialObject
from robotic_library import RoboticProperties

class PrincipalWindow:
    def __init__(self, root:tb.Window):
        # Reference to the main application.
        self.root = root

        # Reference for the Serial Object, for both configuration and connection.
        self.serial_conn = SerialObject()
        self.serial_conn.establish_parameters('COM1', 9600)

        # Robotic properties.
        self.robotic_properties = RoboticProperties()
        
        # ________________________________________________________________________

        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        # - - - - - - - - - - TTK Styles- - - - - - - - - - - -
        # - - - - - - - - - - - - - - - - - - - - - - - - - - - 

        self.entry_dh_params_style = tb.Style()
        self.entry_dh_params_style.configure("dh_params_config.TEntry", 
                                             foreground = 'red', fieldbackground="gray")
        self.entry_dh_params_style.configure("default.TEntry", 
                                             foreground = 'black', fieldbackground="white")

        # ________________________________________________________________________

        # Reference for the handler of the frames.
        self.frames_handler = FrameHandler()

        # Frames used in this application.
        self.main_menu_frame = MainMenuFrame(root, self.frames_handler)
        self.serial_menu_frame = SerialConfigurationFrame(root, self.frames_handler, self.serial_conn)
        self.robotic_configuration_frame = RoboticConfigurationFrame(root, self.frames_handler, self.robotic_properties)
        self.robotic_params_frame = RoboticParamsFrame(root, self.frames_handler, self.robotic_properties)
        self.direct_kinematics_frame = DirectKinematicsFrame(root, self.frames_handler, self.robotic_properties, self.robotic_params_frame)
        self.inverse_kinematics_frame = InverseKinematicsFrame(root, self.frames_handler, self.robotic_properties)

        frames:List[tb.Frame] = [
            self.main_menu_frame,
            self.serial_menu_frame,
            self.robotic_configuration_frame,
            self.robotic_params_frame,
            self.direct_kinematics_frame,
            self.inverse_kinematics_frame
            ]
        
        # Updating the frames container in the Handler. Calling the first frame.
        self.frames_handler.frames = frames
        self.frames_handler.frame_packer('main_frame')

    # -------------------------------------------------------------------------------    

    # -------------------------------------------------------------------------------    

if __name__ == '__main__':

    root = tb.Window()
    root.title("Robot Serial Interface")
    root.geometry('1200x600')
    root.configure(background='#F0ECD2')
    
    principal_window = PrincipalWindow(root)

    root.mainloop()