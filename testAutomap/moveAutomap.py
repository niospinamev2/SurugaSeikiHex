"""
Move Automap

"""

import pic_upv.automaper as automaper
from pic_upv.suruga import System, AxisComponents, Alignment, PowerMeter
import os

# ======================================================
# FUNCIONES
# ======================================================

def guardar_origen(x1, x2):

    with open(ORIGIN_FILE, "w") as f:
        f.write(f"{x1}\n")
        f.write(f"{x2}\n")


def cargar_origen():

    with open(ORIGIN_FILE, "r") as f:
        x1 = float(f.readline())
        x2 = float(f.readline())

    return x1, x2

# ======================================================
# Configuración
# ======================================================

USE_SAVED_ORIGIN = True      # True -> usar origen guardado
SAVE_ORIGIN = False            # Guardar el origen al iniciar

ORIGIN_FILE = "origin.txt"

# Archivo Excel que contiene la información del chip y el plan de medición
EXCEL_FILE = "chipMaps/SurugaTest.xlsx"

# ======================================================
# Inicialización
# ======================================================
# Cargar el chip y el plan de medición desde el archivo Excel
chip, measurement_paths, measurement_plan = automaper.load_chip(
    EXCEL_FILE
)

# Crear el objeto Suruga
suruga = System()
# Crear los objetos AxisComponents para los ejes X1 y X2
x1 = AxisComponents(suruga, "x1")
x2 = AxisComponents(suruga, "x2")

suruga.connect()

# ======================================================
# Se asume que la máquina YA está posicionada sobre WG0
# ======================================================

if USE_SAVED_ORIGIN and os.path.exists(ORIGIN_FILE):

    print("Usando origen almacenado...")

    origin_x1, origin_x2 = cargar_origen()

    x1.move_absolute(origin_x1)
    x2.move_absolute(origin_x2)

else:

    print("Usando posición actual como origen...")

    origin_x1 = x1.get_actual_position()
    origin_x2 = x2.get_actual_position()

    if SAVE_ORIGIN:
        guardar_origen(origin_x1, origin_x2)
        
print("Origen de la máquina")
print(f"X1 = {origin_x1:.3f}")
print(f"X2 = {origin_x2:.3f}")


for measurement in measurement_plan:

    x1_relative = -measurement["input"]["x"]

    x2_relative = -measurement["output"]["x"]

    abs_x1 = origin_x1 + x1_relative

    abs_x2 = origin_x2 + x2_relative

    print("\n" + "=" * 50)

    print(f"Device : {measurement['device']}")

    print(
        f"Input  : {measurement['input']['name']}"
    )

    print(
        f"Output : {measurement['output']['name']}"
    )

    print(
        f"Move X1 -> {abs_x1:.3f}"
    )

    print(
        f"Move X2 -> {abs_x2:.3f}"
    )

    x1.move_absolute(abs_x1)
    x2.move_absolute(abs_x2)

    input("Press Enter to continue...")

# ======================================================
# Volver al origen (WG0)
# ======================================================

print("\n" + "="*40)
print("Regresando a WG0")
print(f"Absoluta : ({origin_x1:.3f}, {origin_x2:.3f})")
print("Relativa : (0.000, 0.000)")

input("Presione Enter para regresar...")

x1.move_absolute(origin_x1)
x2.move_absolute(origin_x2)

print("Movimiento completado.")