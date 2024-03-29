import serial

class SerialConnection:
    # Constructor. Sets the port configuration, connection variable and bias variable for calibration.
    def __init__(self, port_data):
        self.__port_data = port_data
        self.__connection = serial.Serial(timeout=1)

    # Starts the SERIAL connection with the given configuration.
    def __start_port(self):
        self.__close_conn()

        self.__connection.port = self.__port_data.port
        self.__connection.baudrate = self.__port_data.speed

        self.__connection.open()

    # Closes the SERIAL connection.
    def __close_conn(self):
        self.__connection.close()

    # Flushes the SERIAL Buffer and reads a line to throw possible incomplete data.
    def __flush_serial(self):
        self.__connection.flushInput()
        self.__connection.readline()

    # Setting the new port configuration (PUBLIC).
    def port_config(self, new_data):
        self.__port_data = new_data
        print(f'{self.__port_data}\n')
