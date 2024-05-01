import tkinter as tk
from frames_gui import *
from typing import List

# TODO: 
# Here define the window (Already done).
# Define the initial DH parameters and pass them as parameters.
# Define initial configurations for robotics_properties.
# Define initial configurations for serial_configuration.

class FrameHandler:
    def __init__(self):
        self.frames:List[tk.Frame] = []







    # FIXME: Recordar que ahora funciona con strings.
















    def frame_packer(self, frame_name:str):
        '''
        Function used to update the frame that is being selected.
        :selected_frame: is searched in the list of the available frames in order to be loaded. Any other frame is forgoten from the root.
        '''
        for frame in self.frames:
            if frame.name != frame_name:
                frame.pack_forget()
                continue
            frame.pack(expand=True, fill='both')


class PrincipalWindow:
    def __init__(self, root):
        self.root = root

        self.frames_handler = FrameHandler()

        self.main_menu_frame = MainMenuFrame(root, self.frames_handler)
        self.serial_menu_frame = SerialConfigurationFrame(root, self.frames_handler)

        frames:List[tk.Frame] = [
            self.main_menu_frame,
            self.serial_menu_frame,



            ]
        
        # Updating the frames container in the Handler.
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