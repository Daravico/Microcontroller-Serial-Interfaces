from serial import Serial
import serial.tools.list_ports as SerialTools

# ------------
# DESCRIPTION OF LIBRARY:
# ------------

'''
This file can set the configuration for the serial connection. Most of 
the functions require a Serial object to be send as a parameter. In case
it is required, all the functions can be adapted and/or extended within
each section in order to have multiple functionalities or call other 
sections of code.
'''

# ------------------------------------------------------------------------

def get_ports():
    '''
    This function returns the available ports. Needs to be upgraded to 
    reduce the information to be returned.
    '''
    return SerialTools.comports()

# ------------------------------------------------------------------------

def establish_parameters(serial_connection: Serial, port: str, speed: int):
    '''
    This function sets the parameters of the serial comunication. This is
    also useful in case these settings need to be changed.

    :serial_connection(Serial): from the PySerial library, instance that
    establish the serial communication.
    :port(str): sets the designaded serial port.
    :speed(int): baudrate at which the communication will be made.
    '''    
    serial_connection.port = port
    serial_connection.baudrate = speed

# ------------------------------------------------------------------------

def start_connection(serial_connection:Serial, port: str, speed: int):
    '''
    The connection is started, after setting the corresponding parameters.
    Also, it makes sure that there is no current connection with the port.

    :serial_connection(Serial): from the PySerial library, instance that
    establish the serial communication.
    :port(str): sets the designaded serial port.
    :speed(int): baudrate at which the communication will be made.
    '''
    serial_connection.close()
    establish_parameters(serial_connection, port, speed)
    serial_connection.open()

# ------------------------------------------------------------------------

def close_connection(serial_connection:Serial):
    '''
    Closes the connection with the corresponding function. In case another
    configuration is needed it can be added to this method.

    :serial_connection(Serial): from the PySerial library, instance that
    establish the serial communication.
    '''
    serial_connection.close()

# ------------------------------------------------------------------------

def write_message(serial_connection:Serial, message: str):

    '''
    Calling this function to send a message to the serial connection.
    In case something else is required, it can be added to this method.

    :serial_connection(Serial): from the PySerial library, instance that
    establish the serial communication.
    :messgae(str): message to be send. It requires to be encoded to bytes.
    '''
    serial_connection.write(message.encode())

# ------------------------------------------------------------------------

def flush_serial(serial_connection:Serial):
    '''
    Clearing the buffer of the serial connection and reading any remaining 
    data in order to ensure there are no leftovers. 

    :serial_connection(Serial): from the PySerial library, instance that
    establish the serial communication.
    '''
    serial_connection.reset_input_buffer()
    serial_connection.readline()

# ------------------------------------------------------------------------
