import serial_configuration
import serial
import os

# ------------------------------------------------------------------------

def commands_OAT(serial_conn):
    '''
        With this function a single instruction is sent each time to a 
        specific joint, which is selected from the menu that is displayed
        to the user.  

        :serial_connection(Serial): from the PySerial library, instance that
        establish the serial communication.

        return(bool): This return helps in either continuing or exiting 
        the process of this function.
    '''

    # Clearing the screen.
    os.system('cls')

    # Showing the avilable options.
    print("Available:")
    print("[ 1 ] - Q1")
    print("[ 2 ] - Q2")
    print("[ 3 ] - Q3")
    print("[ x ] - Exit")

    # User selection.
    selected_Q = input("Select from the available options: ")

    # In case exit is selected (Any keystroke).
    if selected_Q != '1' and  selected_Q != '2' and  selected_Q != '3':
        os.system('cls')
        return False

    # Angle specification by the user.
    angle = input("Give the angle value (Degrees °): ")

    # The message is prepared and sent through the serial channel.
    instruction = f'Q{selected_Q}-{angle}'
    serial_configuration.write_message(serial_conn, instruction)

    return True

# ------------------------------------------------------------------------

def commands_FULL():
    pass

# ------------------------------------------------------------------------

# Main execution of the program.
if __name__ == '__main__':

    # Clearing the console. If Windows, use 'cls'. Linux use 'clear'.
    os.system('cls')

    # Serial object to establish the Serial connection.
    serial_conn = serial.Serial('COM14', 9600)

    # Main loop.
    while True:
        # Clearing the console, showing the available options of the main menu.
        os.system('cls')
        print("[ 0 ] - Show available ports")
        print("[ 1 ] - Ports Configuration")
        print("[ 2 ] - Send Message")
        print("[ 3 ] - Angular commands (OAT)")
        print("[ 4 ] - Angular commands (FULL)")
        print("[ x ] - Exit\n")

        # Flag to keep looping the submenus unless specified.
        continue_submenu_flag = True
        
        # Selection from the user.
        selection = input("Select mode: ")

        # Showing the available ports.
        # -----------------------------------------------------------------
        if selection == '0':
            for port, desc, _ in sorted(serial_configuration.show_ports()):
                print(f"{port}: {desc}")

        # Changing parameters for the serial communication.
        # -----------------------------------------------------------------
        elif selection == '1':
            port:str = input("PORT: ")
            speed = input("SPEED: ")

            serial_configuration.establish_parameters(serial_conn, port, speed)

        # Sending a specific message.
        # -----------------------------------------------------------------
        elif selection == '2':
            msg = input("Message to send: ")
            serial_conn.write_message(msg)

        # Sub-menu to send single commands to a specific joint.
        # -----------------------------------------------------------------
        elif selection == '3':
            while continue_submenu_flag:
                continue_submenu_flag = commands_OAT(serial_conn)
                
        # Sub-menu to send comands to all the joints. 
        # -----------------------------------------------------------------
        elif selection == '4':
            while continue_submenu_flag:
                pass

        # In case no option is selected, exiting the program. 
        # -----------------------------------------------------------------
        else:
            print("Goodbye . . .")
            break