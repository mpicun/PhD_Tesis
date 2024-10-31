import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def load_dos_file(filename):
    # Leer la primera línea para obtener EFermi
    with open(filename, 'r') as file:
        first_line = file.readline()
        EFermi = float(first_line.split('=')[-1].split()[0])
    
    # Cargar los datos ignorando las líneas comentadas
    data = np.loadtxt(filename, unpack=True, comments='#')
    energy, dos, idos = data[0], data[1], data[2]
    
    # Restar el nivel de Fermi a las energías
    energy = energy - EFermi
    
    return energy, dos, idos

def plot_dos(filenames, x_min=None, x_max=None):
    colors = ['red', 'blue', 'green', 'purple', 'orange']  # Lista de colores para diferentes DOS

    # Crear la gráfica
    plt.figure(figsize=(12, 6))
    
    # Si solo hay un archivo, convertir filenames a lista
    if isinstance(filenames, str):
        filenames = [filenames]
    
    for i, filename in enumerate(filenames):
        # Cargar los datos de DOS y EFermi
        energy, dos, idos = load_dos_file(filename)
        
        # Quitar la parte *_dos.dat del nombre del archivo para la leyenda
        legend_label = os.path.basename(filename).replace('_dos.dat', '')

        # Graficar los DOS con sus respectivos ajustes
        plt.plot(energy, dos, linewidth=0.75, color=colors[i % len(colors)], label=legend_label)
        plt.fill_between(energy, 0, dos, where=(energy < 0), facecolor=colors[i % len(colors)], alpha=0.25)

    # Configurar las etiquetas y el gráfico
    plt.yticks([])
    plt.xlabel('Energía (eV)', fontsize=16)
    plt.ylabel('DOS', fontsize=16)

    # Ajustar los límites del eje X
    if x_min is not None and x_max is not None:
        plt.xlim(x_min, x_max)
    else:
        # Usar el rango de las energías combinadas
        all_energy = np.hstack([load_dos_file(fname)[0] for fname in filenames])
        plt.xlim(all_energy.min(), all_energy.max())
    
    # Ajustar el límite del eje Y automáticamente
    all_dos = np.hstack([load_dos_file(fname)[1] for fname in filenames])
    plt.ylim(0, all_dos.max())

    # Agregar la línea de energía de Fermi en 0 eV para todas las curvas
    plt.axvline(x=0, linewidth=0.5, color='k', linestyle=(0, (8, 10)))

    # Colocar la leyenda en la esquina superior derecha
    plt.legend(loc='upper right', fontsize=16)

    # Agrandar los xticks
    plt.xticks(fontsize=14)

    # Mostrar la gráfica
    plt.show()

if __name__ == "__main__":
    # Verificar si se proporcionan archivos de entrada
    if len(sys.argv) < 2:
        print("Uso: python script.py dos1.dat [dos2.dat ...] [Emin=-6] [Emax=8]")
    else:
        # Extraer archivos DOS y parámetros
        filenames = []
        x_min, x_max = None, None
        
        # Procesar los argumentos
        for arg in sys.argv[1:]:
            if arg.startswith("Emin="):
                x_min = float(arg.split("=")[-1])
            elif arg.startswith("Emax="):
                x_max = float(arg.split("=")[-1])
            else:
                # Si no es un rango, se asume que es un archivo
                filenames.append(arg)
        
        # Graficar los archivos
        plot_dos(filenames, x_min, x_max)

