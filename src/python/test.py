import numpy as np

# Tamaño del array principal
size = 5

# Crear un array NumPy principal de tamaño específico con matrices NumPy 4x4 sin inicializar valores
array = np.array([np.empty((4, 4)) for _ in range(size)])

# Realizar el producto cruz entre todas las matrices 4x4
result = np.eye(4)  # Matriz de resultados inicializada con ceros
for matrix in array:
    result = result @ matrix

print(result)