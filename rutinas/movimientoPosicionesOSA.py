from pic_upv.suruga import System, AxisComponents, Alignment, PowerMeter

from osa_simple import YeniOSA

import matplotlib.pyplot as plt
import time
from datetime import datetime

import os


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

USE_SAVED_ORIGIN = False      # True -> usar origen guardado
SAVE_ORIGIN = True            # Guardar el origen al iniciar

ORIGIN_FILE = "origin.txt"

# ======================================================
# Inicialización
# ======================================================

suruga = System()

# Crear el objeto Alignment
alignment = Alignment(suruga)

#-------------------------------------------------------
x1 = AxisComponents(suruga, "x1")
x2 = AxisComponents(suruga, "x2")

print(x1.attribute)
print(x2.attribute)

#-------------------------------------------------------
flat_left = {
    "main_stage_x": "x1",
    "main_stage_y": "y1",
    "sub_stage_xy": 0,
    "pm_ch": 1,
    "analog_ch": 1,
    "search_range_x": 50,
    "search_range_y": 20,
    "init_range": -30,
}

flat_right = {
    "main_stage_x": "x2",
    "main_stage_y": "y2",
    "sub_stage_xy": 0,
    "pm_ch": 1,
    "analog_ch": 1,
    "search_range_x": 50,
    "search_range_y": 20,
    "init_range": -30,
}

suruga.connect()

# Crear el objeto Power Meter
pm = PowerMeter(suruga)
channel = 1

#------------------------------------------------------
# Configuración del OSA
#------------------------------------------------------

osa = YeniOSA()
osa.connect()

CENTER = 1550
SPAN = 180
RESOLUTION = 0.2
# RESOLUTION = 0.05
SENSITIVITY = -65

osa.setup_sweep(
    center_nm=CENTER,
    span_nm=SPAN,
    resolution_nm=RESOLUTION,
    sensitivity_dbm=SENSITIVITY,
)

# ======================================================
# Posiciones del chip relativas al origen
# ======================================================

waveguides = [
    {"name": "WG0", "x1":   0.0,   "x2":   0.0},
    {"name": "WG1", "x1": -63.5,   "x2": -63.5},
    {"name": "WG2", "x1": -127.0,  "x2": -127.0},
    {"name": "WG3", "x1": -190.5,  "x2": -190.5},
]

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

print()

# ======================================================
# Recorrer todas las waveguides
# ======================================================

for wg in waveguides:

    abs_x1 = origin_x1 + wg["x1"]
    abs_x2 = origin_x2 + wg["x2"]

    print("\n" + "="*40)
    print(f'Guía      : {wg["name"]}')
    print(f'Relativa  : ({wg["x1"]:.3f}, {wg["x2"]:.3f})')
    print(f'Absoluta  : ({abs_x1:.3f}, {abs_x2:.3f})')

    x1.move_absolute(abs_x1)
    x2.move_absolute(abs_x2)

    input("Presione Enter para alinear a la izquierda...")

    print(f"Alineando izquierda - {wg['name']}")

    alignment.set_flat(**flat_left)
    alignment.start_flat()
    alignment.wait_until_complete()

    input("Presione Enter para alinear a la derecha...")

    print(f"Alineando derecha - {wg['name']}")

    alignment.set_flat(**flat_right)
    alignment.start_flat()
    alignment.wait_until_complete()

    power = pm.get_power(channel)
    print(f"Potencia: {power}")

    osa.run_sweep(
    trace=1,
    averages=1,
    progress_poll_s=0.5,
    start_delay_s=2.0,
    )

    time.sleep(2)

    trace = osa.get_trace(1)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"data_osa/medicion_001_{timestamp}_{wg['name']}.txt"

    trace.save_txt(filename)

    input("Presione Enter para continuar...")

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

osa.close()

print("Movimiento completado.")
