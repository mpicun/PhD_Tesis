#!/usr/bin/python3
from ase.visualize import view
from ase.io import read
import sys

def main():
    if len(sys.argv) != 3:
        print("Uso: python script.py POSCAR bader.dat")
        sys.exit(1)

    poscar_file = sys.argv[1]
    bader_file = sys.argv[2]

    # Leer la estructura del archivo POSCAR
    structure = read(poscar_file)
    num_atoms = len(structure)

    # Leer las cargas del archivo bader.out
    charges = []
    with open(bader_file, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.strip():  # Ignorar líneas vacías
                try:
                    parts = line.split()
                    if len(parts) == 2:
                        charge = float(parts[1].strip())
                        charges.append(charge)
                except Exception as e:
                    print(f"Error en la línea {i + 1}: {line.strip()} - {e}")

    # Eliminar líneas adicionales si hay más cargas que átomos
    if len(charges) > num_atoms:
        charges = charges[:num_atoms]

    # Verificar que la longitud de las cargas coincida con el número de átomos
    assert len(charges) == num_atoms, "El número de cargas no coincide con el número de átomos en la estructura"

    # Asignar las cargas a la estructura
    structure.set_initial_charges(charges)

    # Guardar las cargas en un archivo de salida
    with open('bader_charges.dat', 'w') as f:
        for i, charge in enumerate(charges):
            atom = structure[i]
            f.write(f"{atom.symbol} {i + 1}: {charge:.6f}\n")

    print("Cargas guardadas en 'bader_charges.dat'")

    # Visualizar la estructura con ASE GUI
    view(structure)

if __name__ == "__main__":
    main()

