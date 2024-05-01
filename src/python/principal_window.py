import tkinter as tk
from frames_gui import *
from typing import List

# TODO: 
# Here define the window (Already done).
# Define the initial DH parameters and pass them as parameters.
# Define initial configurations for robotics_properties.
# Define initial configurations for serial_configuration.

class PrincipalWindow:
    def __init__(self, root):
        self.root = root

        self.main_menu_frame = MainMenuFrame(root)
        self.serial_menu_frame = SerialConfigurationFrame(root)

        self.frames = [
            self.main_menu_frame,
            self.serial_menu_frame
            ]
        
        self.frame_packer(self.main_menu_frame)

    # -------------------------------------------------------------------------------    

    def frame_packer(self, selected_frame:tk.Frame):
        '''
        Function used to update the frame that is being selected.
        :selected_frame: is searched in the list of the available frames in order to be loaded. Any other frame is forgoten from the root.
        '''
        for frame in self.frames:
            if frame != selected_frame:
                frame.pack_forget()
                continue
            frame.pack(expand=True, fill='both')

    # -------------------------------------------------------------------------------    

if __name__ == '__main__':

    root = tk.Tk()
    root.title("Robot Serial Interface")
    root.geometry('1200x600')
    root.configure(background='#F0ECD2')
    
    principal_window = PrincipalWindow(root)

    root.mainloop()