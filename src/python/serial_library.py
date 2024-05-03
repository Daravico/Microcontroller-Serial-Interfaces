from serial import Serial
import serial.tools.list_ports as SerialTools

class SerialObject(Serial):
    def __init__(self):
        Serial.__init__(self)

        self.available_ports_data = {}

# -----------------------------------------------------------------------------------------------------------------------------

    def get_ports(self):
        '''
        This function returns the available ports. Needs to be upgraded to 
        reduce the information to be returned.
        '''
        return SerialTools.comports()

# -----------------------------------------------------------------------------------------------------------------------------

    def establish_parameters(self, port: str, speed: int):
        '''
        This function sets the parameters of the serial comunication. This is
        also useful in case these settings need to be changed.

        :port(str): sets the designaded serial port.
        :speed(int): baudrate at which the communication will be made.
        '''    
        self.port = port
        self.baudrate = speed

# -----------------------------------------------------------------------------------------------------------------------------

    ## MOST OF THE FUNCTIONS DONT REQUIRE TO BE CALLED. 
    # MAKE THIS SIMPLER, SINCE IT IMPORTS THE CONFIGURATION FROM "SERIAL"
    # ADD THE FUNCTIONS TO SEND THE MESSAGES WITH THE CORRECT CONFIGURATION/ENCODING.
    # PREPARE READABILITY OF DATA (NOT FOR THIS PROJECT MAYBE.)