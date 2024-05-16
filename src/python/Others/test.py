import serial
import time

# Configurar el puerto serial (ajusta el puerto según tu configuración)
puerto_serial ='COM1'  # Linux
# puerto_serial = 'COM3'  # Windows

# Inicializar la comunicación serial
ser = serial.Serial(puerto_serial, 9600, timeout=1)

# Esperar un breve momento para la inicialización
time.sleep(2)

# Enviar el mensaje
mensaje = "B"
ser.write(mensaje.encode())

# Cerrar la conexión serial
ser.close()
