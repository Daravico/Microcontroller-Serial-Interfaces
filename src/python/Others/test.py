'''
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
'''
import tkinter as tk
from tkinter import ttk

class TablaDH:
    def __init__(self, master):
        self.master = master
        self.master.title("Tabla de parámetros DH")

        self.frame = ttk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        self.encabezados = ['a', 'alpha', 'd', 'theta']
        self.tabla = []
        for i, encabezado in enumerate(self.encabezados):
            label = ttk.Label(self.frame, text=encabezado)
            label.grid(row=0, column=i, padx=5, pady=5)

        for i in range(1, 4):  # Crear filas
            fila = []
            for j in range(4):  # Crear columnas
                validar_numeros = self.master.register(self.validar_entrada)
                entry = ttk.Entry(self.frame, validate="all", validatecommand=(validar_numeros, "%P", "%V"))
                entry.grid(row=i, column=j, padx=5, pady=5)
                entry.bind("<FocusOut>", self.validar_salida_foco)
                fila.append(entry)
            self.tabla.append(fila)

    def validar_entrada(self, valor, motivo):
        if motivo == "focusout":  # Si el evento es focusout
            self.validar_salida_foco()
            return True
        elif valor == "" or valor.replace(".", "", 1).isdigit():
            return True
        elif valor == "":  # Si el valor está vacío después de borrar manualmente
            return True
        else:
            return False

    def validar_salida_foco(self, event=None):
        for fila in self.tabla:
            for entry in fila:
                if entry.get() == "":
                    entry.insert(0, "0")

def main():
    root = tk.Tk()
    app = TablaDH(root)
    root.mainloop()

if __name__ == "__main__":
    main()
