import tkinter as tk
from tkinter import ttk
import time

def start_progress():
    progress_bar.start(50)  # La duración total es de 5000 milisegundos (5 segundos)
    root.after(5000, stop_progress)  # Detiene el progreso después de 5 segundos

def stop_progress():
    progress_bar.stop()

root = tk.Tk()
root.title("ProgressBar")

# Crear ProgressBar
progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")

# Colocar ProgressBar en la ventana
progress_bar.pack(pady=10)

# Crear botón para iniciar el progreso
start_button = tk.Button(root, text="Iniciar Progreso", command=start_progress)
start_button.pack(pady=5)

root.mainloop()
