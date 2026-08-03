"""
===============================================================================
Bla
===============================================================================

Purpose
-------
Incluir informacion de alineamiento como posicion alcanzada y estatus de alinea-
miento

Workflow
--------


Usage
-----


Output
------


Requirements
------------


===============================================================================
"""

from pic_upv.suruga import System, AxisComponents, Alignment, PowerMeter
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
import time
import numpy as np
import os
import csv

# ======================================================
# FUNCIONES
# ======================================================

def wait(message="Press Enter to continue...", delay=0):
    """
    Pause execution depending on the execution mode.

    Parameters
    ----------
    message : str
        Message displayed in debug mode.
    delay : float
        Waiting time in seconds when running in automatic mode.

    Examples
    --------
    Wait for user confirmation in interactive mode or continue
    immediately in automatic mode.

    >>> wait("Press Enter to start the OSA...")

    Wait for user confirmation in interactive mode or 5 seconds
    in automatic mode.

    >>> wait("Press Enter to continue...", delay=5)

    Wait 2 seconds only when running in automatic mode.

    >>> wait(delay=2)
    """
    if DEBUG_MODE:
        input(message)
    elif delay > 0:
        time.sleep(delay)


def guardar_origen(x1, x2):

    with open(ORIGIN_FILE, "w") as f:
        f.write(f"{x1}\n")
        f.write(f"{x2}\n")


def cargar_origen():

    with open(ORIGIN_FILE, "r") as f:
        x1 = float(f.readline())
        x2 = float(f.readline())

    return x1, x2

def move_xy_safe(x1, x2, y1, y2, target_x1, target_x2, target_y1, target_y2, clearance=10):

    try:
        y1.move_absolute(target_y1 + clearance)
        y2.move_absolute(target_y2 + clearance)

        time.sleep(1)

        x1.move_absolute(target_x1)
        x2.move_absolute(target_x2)

        time.sleep(1)

    finally:
        y1.move_absolute(target_y1)
        y2.move_absolute(target_y2)

# ======================================================
# Configuración
# ======================================================

DEBUG_MODE = False             # True -> modo debug, False -> modo automático
USE_SAVED_ORIGIN = False      # True -> usar origen guardado
SAVE_ORIGIN = True            # Guardar el origen al iniciar


FILE_NAME = "originTest.txt"  # Nombre del archivo donde guardaremos las coordenadas de origen
ORIGIN_FILE = "data/origin/" + FILE_NAME

# Numero de veces que se repetirá la medición de todos los dispositivos
num_repeticiones = 1

# ======================================================
# Inicialización
# ======================================================

#-------------------------------------------------------
# Crear el objeto Suruga
#-------------------------------------------------------
suruga = System()
#-------------------------------------------------------
# Crear el objeto Alignment
#-------------------------------------------------------
alignment = Alignment(suruga)
#-------------------------------------------------------
# Crear los objetos AxisComponents para los ejes X1 y X2
#-------------------------------------------------------
x1 = AxisComponents(suruga, "x1")
x2 = AxisComponents(suruga, "x2")
y1 = AxisComponents(suruga, "y1")
y2 = AxisComponents(suruga, "y2")
z1 = AxisComponents(suruga, "z1")
z2 = AxisComponents(suruga, "z2")

#-------------------------------------------------------
# Definir los parámetros de alineamiento para el brazo
# izquierdo y derecho
#-------------------------------------------------------

flat_left = {
    "main_stage_x": "x1",
    "main_stage_y": "z1",
    "sub_stage_xy": 0,
    "pm_ch": 1,
    "analog_ch": 1,
    "search_range_x": 50,
    "search_range_y": 50,
    "field_pitch_x": 0.5,
    "field_pitch_y": 0.5,
    "init_range": -40,
}

flat_right = {
    "main_stage_x": "x2",
    "main_stage_y": "z2",
    "sub_stage_xy": 0,
    "pm_ch": 1,
    "analog_ch": 1,
    "search_range_x": 50,
    "search_range_y": 50,
    "field_pitch_x": 0.5,
    "field_pitch_y": 0.5,
    "init_range": -40,
}


#-------------------------------------------------------
# Concectarse a la plataforma suruga
#------------------------------------------------------
suruga.connect()

#-------------------------------------------------------
# Crear el objeto PowerMeter
#-------------------------------------------------------
pm = PowerMeter(suruga)
channel = 1

# ======================================================
# Posiciones del chip relativas al origen
# ======================================================

target_y1 = y1.get_actual_position()
target_y2 = y2.get_actual_position()

waveguides = [
    {"name": "WG0", "x1":   0.0,   "x2":   0.0},
    {"name": "WG1", "x1": -126.5,  "x2": -126.5},
    {"name": "WG2", "x1": -253.0,  "x2": -253.0},
    {"name": "WG3", "x1": -379.5,  "x2": -379.5},
]

# ======================================================
# Logica para definir el punto de origen del sistema, si 
# se va a usar el origen guardado o la posición actual,
# la posicion de inicio siempre deberá ser WG0
# ======================================================

if USE_SAVED_ORIGIN and os.path.exists(ORIGIN_FILE):

    print("Usando origen almacenado...")

    origin_x1, origin_x2 = cargar_origen()

    move_xy_safe(
        x1,
        x2,
        y1,
        y2,
        origin_x1,
        origin_x2,
        target_y1,
        target_y2,
        clearance=10,
    )

else:

    print("Usando posición actual como origen...")

    origin_x1 = x1.get_actual_position()
    origin_x2 = x2.get_actual_position()

    if SAVE_ORIGIN:
        guardar_origen(origin_x1, origin_x2)
        
print("Origen de la máquina")
print(f"X1 = {origin_x1:.3f}")
print(f"X2 = {origin_x2:.3f}")


# ======================================================
# Crear carpeta y archivo
# ======================================================

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

filename = "vertical-" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
filepath = data_folder / filename

header = [
    "Fecha",
    "Repeticion",
    "Waveguide",
    "Power_dBm",
    "x1",
    "y1",
    "z1",
    "status_left",
    "x2",
    "y2",
    "z2",
    "status_right",
]

with open(filepath, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

print(f"\nArchivo creado: {filepath}")

# ======================================================
# Repeticiones
# ======================================================

wait("Press Enter to start...")

for repeticion in range(num_repeticiones):

    # Indicador del número de repeticiones
    print("\n" + "=" * 50)
    print(f"Repetición {repeticion + 1}/{num_repeticiones}")

    fila = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

    for wg in waveguides:

        abs_x1 = origin_x1 + wg["x1"]
        abs_x2 = origin_x2 + wg["x2"]

        print("\n" + "=" * 40)
        print(f'Guía      : {wg["name"]}')
        print(f'Absoluta  : ({abs_x1:.3f}, {abs_x2:.3f})')


        move_xy_safe(x1, x2, y1, y2, abs_x1, abs_x2, target_y1, target_y2)

        time.sleep(1)

        print("Alineando izquierda...")

        alignment.set_flat(**flat_left)
        alignment.start_flat()
        estado_left = alignment.wait_until_complete()

        time.sleep(1)

        print("Alineando derecha...")

        alignment.set_flat(**flat_right)
        alignment.start_flat()
        estado_right = alignment.wait_until_complete()

        time.sleep(1)

        medidas = []

        for i in range(10):
            medidas.append(pm.get_power(channel))
            time.sleep(0.1)

        power = np.mean(medidas)

        time.sleep(1)

        print(f"Potencia: {power:.6f}")

        #---------------------------------------------------
        # Solicitar confirmación del usuario para continuar 
        # con la siguiente medición
        #--------------------------------------------------- 
            
        # DEBUG
        wait("Press Enter to continue with next measurement...")

        #---------------------------------------------------
        # Guardar en el CSV la información de la guía
        #---------------------------------------------------

        with open(filepath, "a", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                repeticion + 1,
                wg["name"],
                power,

                x1.get_actual_position(),
                y1.get_actual_position(),
                z1.get_actual_position(),
                estado_left,

                x2.get_actual_position(),
                y2.get_actual_position(),
                z2.get_actual_position(),
                estado_right,
            ])

    # ------------------------------------------------------
    # Retornar al origen (WG0) después de completar todas las mediciones
    # ------------------------------------------------------        

    print("Regresando a WG0...")

    move_xy_safe(
        x1,
        x2,
        y1,
        y2,
        origin_x1,
        origin_x2,
        target_y1,
        target_y2,
        clearance=10,
    )