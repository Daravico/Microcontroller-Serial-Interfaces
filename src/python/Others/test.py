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
                # Pasar argumentos adicionales al bind de FocusOut utilizando una función lambda
                entry.bind("<FocusOut>", lambda event, fila=i, columna=j: self.validar_salida_foco(event, fila, columna))
                fila.append(entry)
            self.tabla.append(fila)

    def validar_entrada(self, valor, motivo):
        #if motivo == "focusout":  # Si el evento es focusout
        #    return True
            # Llamar a validar_salida_foco con los parámetros adecuados
        #    self.validar_salida_foco(None, None, None)
        #    return True
        if valor == "" or valor.replace(".", "", 1).isdigit():
            return True
        elif valor == "-":  # Permitir solo un signo negativo al principio
            return True
        elif valor.replace(".", "", 1).isdigit() or (valor.startswith("-") and valor[1:].replace(".", "", 1).isdigit()):
            return True
        else:
            return False

    def validar_salida_foco(self, event, fila, columna):
        print("Se perdió el foco en la fila {}, columna {}".format(fila, columna))

def main():
    root = tk.Tk()
    app = TablaDH(root)
    root.mainloop()

if __name__ == "__main__":
    main()
