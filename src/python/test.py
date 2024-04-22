import numpy as np

# Tamaño del array exterior
size = 5

# Crear un array NumPy de tamaño específico con arrays NumPy sin inicializar valores
array = np.array([np.empty((3,3)) for _ in range(size)])

print(array)