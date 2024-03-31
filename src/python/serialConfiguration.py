from serial import Serial
import serial.tools.list_ports as SerialTools

def show_ports():
    '''
    This function returns the available ports. Needs to be upgraded to 
    reduce the information to be returned.
    '''
    return SerialTools.comports()

def establish_parameters(serial_connection: Serial, port: str, speed: int):
    '''
    This function sets the parameters of the serial comunication.

    :serial_connection(Serial): from the PySerial library, instance that
    establish the serial communication.
    :port(str): sets the designaded serial port.
    :speed(int): baudrate at which the communication will be made.
    '''    
    serial_connection.port = port
    serial_connection.baudrate = speed

def start_connection(serial_connection:Serial, port: str, speed: int):
    serial_connection.close()
    establish_parameters(serial_connection, port, speed)
    serial_connection.open()

def close_connection(serial_connection:Serial):
    serial_connection.close()

def write_message(serial_connection:Serial, message: str):
    serial_connection.write(message.encode())

def flush_serial(serial_connection:Serial):
    serial_connection.reset_input_buffer()
    serial_connection.readline()
