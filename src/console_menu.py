
from serialConfig import PortsInfo
from serialObject import SerialConnection

import serialObject

from serialConfiguration import SerialConnection

if __name__ == '__main__':

    serial_conn = SerialConnection()

    while True:
        print("[ 0 ] - Show available ports")
        print("[ 1 ] - Ports Configuration")
        print("[ 2 ] - Send Message")
        print("[ x ] - Exit\n")

        entry = input("Select mode: ")

        if entry == '0':
            serial_conn.show_ports()

        elif entry == '1':
            serial_conn.show_ports()

            port = input("PORT: ")
            speed = input("SPEED: ")

            serial_conn.establish_parameters(port, speed)

        elif entry == '2':
            msg = input("MSG: ")
            serial_conn.write_message(msg)

        else:
            print("Goodbye . . .")
            break