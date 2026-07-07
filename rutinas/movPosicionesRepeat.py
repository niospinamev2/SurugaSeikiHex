from pathlib import Path
from datetime import datetime
import time

from pic_upv.suruga import System, AxisComponents, Alignment, PowerMeter

# ======================================================
# Configuración
# ======================================================

num_repeticiones = 2
channel = 1

# ======================================================
# Inicialización
# ======================================================

suruga = System()

alignment = Alignment(suruga)

x1 = AxisComponents(suruga, "x1")
x2 = AxisComponents(suruga, "x2")

print(x1.attribute)
print(x2.attribute)

flat_left = {
    "main_stage_x": "x1",
    "main_stage_y": "y1",
    "sub_stage_xy": 0,
    "pm_ch": 1,
    "analog_ch": 1,
    "search_range_x": 50,
    "search_range_y": 20,
    "init_range": -20,
}

flat_right = {
    "main_stage_x": "x2",
    "main_stage_y": "y2",
    "sub_stage_xy": 0,
    "pm_ch": 1,
    "analog_ch": 1,
    "search_range_x": 50,
    "search_range_y": 20,
    "init_range": -20,
}

suruga.connect()

pm = PowerMeter(suruga)

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

origin_x1 = x1.get_actual_position()
origin_x2 = x2.get_actual_position()

print("Origen de la máquina")
print(f"X1 = {origin_x1:.3f}")
print(f"X2 = {origin_x2:.3f}")

# ======================================================
# Crear carpeta y archivo
# ======================================================

data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"
filepath = data_folder / filename

header = ["Fecha"] + [wg["name"] for wg in waveguides]

with open(filepath, "w", encoding="utf-8") as f:
    f.write("\t".join(header) + "\n")

print(f"\nArchivo creado: {filepath}")

# ======================================================
# Repeticiones
# ======================================================

for repeticion in range(num_repeticiones):

    print("\n" + "=" * 50)
    print(f"Repetición {repeticion + 1}/{num_repeticiones}")

    fila = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]

    for wg in waveguides:

        abs_x1 = origin_x1 + wg["x1"]
        abs_x2 = origin_x2 + wg["x2"]

        print("\n" + "=" * 40)
        print(f'Guía      : {wg["name"]}')
        print(f'Absoluta  : ({abs_x1:.3f}, {abs_x2:.3f})')

        x1.move_absolute(abs_x1)
        x2.move_absolute(abs_x2)

        time.sleep(1)

        print("Alineando izquierda...")

        alignment.set_flat(**flat_left)
        alignment.start_flat()
        alignment.wait_until_complete()

        time.sleep(1)

        print("Alineando derecha...")

        alignment.set_flat(**flat_right)
        alignment.start_flat()
        alignment.wait_until_complete()

        time.sleep(1)

        power = pm.get_power(channel)

        time.sleep(1)

        print(f"Potencia: {power:.6f}")

        fila.append(f"{power:.6f}")

    with open(filepath, "a", encoding="utf-8") as f:
        f.write("\t".join(fila) + "\n")

    print("Regresando a WG0...")

    x1.move_absolute(origin_x1)
    x2.move_absolute(origin_x2)
