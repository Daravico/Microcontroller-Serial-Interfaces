import serial


ser = serial.Serial('COM13', 9600, timeout=10)
ser.close()
ser.open()

ser.write(b'Q174.56')

texto = ser.readline()
print(texto)
ser.close()