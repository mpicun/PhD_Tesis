import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Parámetros
laser = 633.0 # nm
temperature = 25.0 # °C
dw = 5 # cm⁻¹ (ancho de la lorentziana)
w0 = 10**7 / laser # nm to cm⁻¹
wt = (temperature + 273.15) * (207.3 / 298.15)  # cm⁻¹ (frecuencia de energía térmica)

def main(folder_path):
    # Ruta del archivo Excel
    file_path = os.path.join(folder_path, 'raman_data.xlsx')

    # Leer el archivo Excel
    df = pd.read_excel(file_path)

    # Eje x: rango de frecuencias para el espectro
    w = np.arange(0, 1100, 1)  # cm⁻¹

    # Inicializar el eje y (intensidad del espectro Raman)
    raman_spectrum = np.zeros(len(w))

    # Guardar las posiciones de los picos para etiquetar las simetrías
    peak_positions = []
    symmetries = []
    peak_intensities = []

    # Loop sobre cada modo Raman en el Excel
    for _, row in df.iterrows():
        freq = row['Frequency (cm-1)']
        intensity = row['Raman Intensity (A^4/amu)']
        symmetry = row['Symmetry']
        
        # Calcular y agregar la contribución de cada modo Raman al espectro total
        raman_spectrum += intensity * ((w0 - freq)**4 / (freq * (1 - np.exp(-freq / wt)))) * (dw / ((freq - w)**2 + dw**2))

        # Guardar la frecuencia, simetría e intensidad del pico para etiquetar más tarde
        peak_positions.append(freq)
        symmetries.append(symmetry)
        peak_intensities.append(intensity)

    # Normalizar el espectro Raman
    raman_spectrum /= np.max(raman_spectrum)

    # Guardar el espectro simulado en un archivo Excel
    output_df = pd.DataFrame({'Frequency (cm-1)': w, 'Intensity (normalized)': raman_spectrum})
    output_file = os.path.join(folder_path, 'simulated_raman.xlsx')
    output_df.to_excel(output_file, index=False)
    print(f'Archivo Excel con el espectro simulado generado: {output_file}')

    # Graficar el espectro
    plt.plot(w, raman_spectrum)
    plt.xlabel('Frequency (cm⁻¹)')
    plt.ylabel('Intensity (normalized)')
    plt.title('Simulated Raman Spectrum')

    # Etiquetar los picos con la simetría, ajustando ligeramente la posición
    for freq, symmetry, intensity in zip(peak_positions, symmetries, peak_intensities):
        peak_y = raman_spectrum[int(freq)]  # Obtener la intensidad correspondiente en el espectro
        plt.text(freq + 10, peak_y + 0.02, symmetry, fontsize=8, ha='center')  # Desplazamos un poco a la derecha y arriba

    # Mostrar el gráfico
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Uso: python script.py <folder_path>')
    else:
        main(sys.argv[1])

