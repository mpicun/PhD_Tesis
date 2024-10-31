import os
import re
import pandas as pd
import sys

def extract_raman_modes_phout(ph_out_file):
    raman_modes = []
    with open(ph_out_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.search(r'freq\s+\(\s*(\d+)\s*-\s*\d+\)\s*=\s*([\d.-]+)\s*\[cm-1\]\s*-->\s*(\w+)\s*R', line)
            if match:
                mode_number = int(match.group(1))
                symmetry = match.group(3)
                raman_modes.append((mode_number, symmetry))
    return raman_modes

def get_frequency_intensity_dmout(dm_out_file, mode_number):
    with open(dm_out_file, 'r') as file:
        lines = file.readlines()
        for line in lines:
            match = re.search(r'^\s*{}\s+([\d.-]+)\s+[\d.-]+\s+[\d.-]+\s+([\d.-]+)'.format(mode_number), line)
            if match:
                frequency = float(match.group(1))
                intensity = float(match.group(2))
                return frequency, intensity
    return None, None

def generate_raman_excel(ph_out_file, dm_out_file, output_file):
    # Extraer los modos Raman activos desde el archivo ph.out
    raman_modes = extract_raman_modes_phout(ph_out_file)

    # Crear lista para almacenar los datos del Excel
    raman_data = []

    # Obtener la frecuencia e intensidad desde el archivo dm.out
    for mode_number, symmetry in raman_modes:
        frequency, intensity = get_frequency_intensity_dmout(dm_out_file, mode_number)
        if frequency is not None and intensity is not None and intensity != 0:
            raman_data.append((mode_number, symmetry, frequency, intensity))

    # Crear DataFrame
    df = pd.DataFrame(raman_data, columns=['Mode Number', 'Symmetry', 'Frequency (cm-1)', 'Raman Intensity (A^4/amu)'])

    # Guardar en un archivo Excel
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <carpeta>")
        sys.exit(1)

    # Obtener la carpeta desde la línea de comando
    folder = sys.argv[1]

    # Comprobar si existen los archivos ph.out y dm.out en la carpeta
    ph_out_path = os.path.join(folder, "ph.out")
    dm_out_path = os.path.join(folder, "dm.out")

    if not os.path.exists(ph_out_path) or not os.path.exists(dm_out_path):
        print("Error: No se encontraron los archivos ph.out o dm.out en la carpeta proporcionada.")
        sys.exit(1)

    # Definir el nombre de salida del archivo Excel
    output_excel = os.path.join(folder, "raman_data.xlsx")

    # Ejecutar el proceso
    generate_raman_excel(ph_out_path, dm_out_path, output_excel)

    print(f"Archivo Excel generado: {output_excel}")

