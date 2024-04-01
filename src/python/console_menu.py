import serial_configuration
import serial
import os

def commands_OAT(serial_conn):
    os.system('cls')

    print("Available:")
    print('[1] - Q1')
    print('[2] - Q2')
    print('[3] - Q3')

    selected_Q = input("Select from the available Q:")
    angle = input("Give the angle value (Degrees °):")

    instruction = f'Q{selected_Q}-{angle}'
    serial_configuration.write_message(serial_conn, instruction)

def commands_FULL():
    pass


# Main execution of the program.
if __name__ == '__main__':

    # Clearing the console. If Windows, use 'cls'. Linux use 'clear'.
    os.system('cls')

    # Serial object to establish the Serial connection.
    serial_conn = serial.Serial()

    # Main loop.
    while True:
        print("[ 0 ] - Show available ports")
        print("[ 1 ] - Ports Configuration")
        print("[ 2 ] - Send Message")
        print("[ 3 ] - Angular commands (OAT)")
        print("[ 4 ] - Angular commands (FULL)")
        print("[ x ] - Exit\n")

        # Selection from the user.
        selection = input("Select mode: ")

        if selection == '0':
            for port, desc, _ in sorted(serial_configuration.show_ports()):
                print(f"{port}: {desc}")

        elif selection == '1':
            port:str = input("PORT: ")
            speed = input("SPEED: ")

            serial_configuration.establish_parameters(serial_conn, port, speed)

        elif selection == '2':
            msg = input("Message to send: ")
            serial_conn.write_message(msg)

        elif selection == '3':
            while True:
                pass

        elif selection == '4':
            while True:
                pass

        else:
            print("Goodbye . . .")
            break