from serial import Serial
import serial.tools.list_ports as SerialTools

class SerialConfiguration(Serial):
    def __init__(self):
        Serial.__init__()

    
    
    
    def get_ports():
        '''
        This function returns the available ports. Needs to be upgraded to 
        reduce the information to be returned.
        '''
        return SerialTools.comports()
    

    ## MOST OF THE FUNCTIONS DONT REQUIRE TO BE CALLED. 
    # MAKE THIS SIMPLER, SINCE IT IMPORTS THE CONFIGURATION FROM "SERIAL"
    # ADD THE FUNCTIONS TO SEND THE MESSAGES WITH THE CORRECT CONFIGURATION/ENCODING.
    # PREPARE READABILITY OF DATA (NOT FOR THIS PROJECT MAYBE.)