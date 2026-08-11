"""
===============================================================================
Raster Scan with Heatmap and Automatic Centering
===============================================================================

Purpose
-------
Perform a two-dimensional raster scan by moving one axis in discrete steps while
acquiring a profile along the orthogonal axis at each position.

The script generates an interactive heatmap from the acquired profiles,
optionally stores the raw profile data, and can automatically reposition the
stages at the location where the maximum optical signal was measured.

===============================================================================
"""

from datetime import datetime
import json
from pathlib import Path

import numpy as np
import plotly.graph_objects as go

from pic_upv.suruga import AxisComponents, Profile, System

# ======================================================
# Condiciones de ejecución
# ======================================================

# Selecciona si se almacenan los datos crudos de cada perfil en TXT.
SAVE_PROFILE_TXT = True

# Tras generar el mapa, mueve X y Z al punto cuya señal 1 fue máxima.
MOVE_TO_MAX_POWER = True

# ======================================================
# FUNCIONES
# ======================================================
# Esta función la tomamos de profileViewer.py para filtrar la información obtenida
# de la plataforma suruga
def clean_profile_data(data: dict) -> tuple[np.ndarray, np.ndarray]:
    """Return valid profile samples sorted by position."""

    positions = np.asarray(data["main_position"], dtype=float)
    signal = np.asarray(data["signal1"], dtype=float)

    measured = np.isfinite(positions) & np.isfinite(signal) & (positions != 0)

    if not np.any(measured):
        raise RuntimeError("The profile contains no valid samples.")

    positions = positions[measured]
    signal = signal[measured]

    order = np.argsort(positions)
    return positions[order], signal[order]

# El proceso de captura de perfil en un documento de texto llevado a cabo en RasterScanV2
# se encapsula en una función, Nota: hay un problema con ladefinición del header, que depende
# de parámetros globales

def save_profile_txt(
    filepath: Path,
    index: int,
    data: dict,
    metadata: dict,
    center_x: float,
    center_z: float,
) -> None:
    """Guarda un profile completo en el mismo formato usado por RasterScanV2."""
    matrix = np.column_stack(
        [
            data["main_position"],
            data["sub1_position"],
            data["sub2_position"],
            data["signal1"],
            data["signal2"],
        ]
    )
    header = (
        f"Profile: {index:03d}\n"
        f"Date: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
        f"Center X: {center_x:.3f} um\n"
        f"Center Z: {center_z:.3f} um\n"
        f"Arm: {metadata['arm']}\n"
        # -------------------------------------------
        f"Scan axis: {metadata['scan_axis']}\n"
        f"Scan width: {metadata['scan_width']} um\n"
        f"Scan step: {metadata['scan_step']} um\n"
        # -------------------------------------------
        f"Profile axis: {metadata['profile_axis']}\n"
        f"Profile range: {metadata['profile_range']} um\n"
        f"Profile speed: {metadata['profile_speed']} um/s\n\n"
        "main_position\tsub1_position\tsub2_position\tsignal1\tsignal2"
    )
    np.savetxt(filepath, matrix, delimiter="\t", header=header, comments="# ")

def create_heatmap(scan_data: list[dict], output_path: Path) -> dict:
    """Crea el HTML interactivo y devuelve la posición del máximo medido."""
    # Primero es necesario verificar que exista dictado con la informacion de los perfiles.
    if not scan_data:
        raise RuntimeError("No se ha adquirido ningún profile; no se puede crear el mapa.")
    # Por defecto se espera que scan data tenga la siguiente estructura:
    # {
    #     "x": ...,
    #     "z_positions": ...,
    #     "signal": ...
    # }
    # El Perfil se ejecuto en el eje Z, para el mapa es necesario asegurar que todos
    # los perfiles de potencia tengan el mismo eje Z común. 
    z_common = scan_data[0]["z_positions"]
    # Entrega un arreglo de numpy con todas las posiciones en X donde se tomaron los 
    # perfiles de potencia
    x_positions = np.asarray([entry["x"] for entry in scan_data], dtype=float)
    heatmap_rows = []
    # Al ejecutar el codigo se busca que quede algo mas o menos una lista de
    # arrays 1D:
    # heatmap_rows = [
    #     [a, b, c, d, e],
    #     [f, g, h, i, j],
    #     [k, l, m, n, o],
    # ]

    best = None # Dejaremos esta variable para encontrar el maximo global

    # Recorrer todos los perfiles de potencia y construir la matriz de datos para el mapa de calor
    for entry in scan_data:
        z_positions = entry["z_positions"]
        signal = entry["signal"]

        # Se usa la función interp de numpy para obtener los valores de signal en las posiciones
        # de z_common
        heatmap_rows.append(np.interp(z_common, z_positions, signal))

        # Retornar el índice donde se encuentra el máximo de potencia en el perfil actual
        max_index = int(np.argmax(signal))
        candidate = {
            "x": float(entry["x"]),
            "z": float(z_positions[max_index]), # Valor de z en el índice del máximo
            "signal1": float(signal[max_index]), # Valor de la señal en el índice del máximo
        }

        # Se lleva una comparación conel mejor máximo global encontrado
        # hasta el momento 
        if best is None or candidate["signal1"] > best["signal1"]:
            best = candidate

    # Convertir la lista de filas en un arreglo 2D de numpy
    heatmap = np.asarray(heatmap_rows)

    figure = go.Figure(
        go.Heatmap(
            x=z_common,
            y=x_positions,
            z=heatmap,
            colorscale="Viridis",
            colorbar_title="Signal 1 (V)",
        )
    )
    figure.update_layout(
        title="Raster scan",
        xaxis_title="Z position (µm)",
        yaxis_title="X position (µm)",
        template="plotly_white",
    )
    figure.write_html(output_path, include_plotlyjs="cdn")

    # Devuelve el mejor valor obtenido de todo el barrido
    # {
    #     "x": 127.0,
    #     "z": 1532.5,
    #     "signal1": 0.842
    # }
    return best

# ======================================================
# Configuración del barrido
# ======================================================

ARM = 1                     # 1 = brazo izquierdo | 2 = brazo derecho
SCAN_AXIS = f"x{ARM}"
PROFILE_AXIS = f"z{ARM}"
PROFILE_RANGE = 50          # µm
PROFILE_SPEED = 25          # µm/s
SCAN_WIDTH = 50             # µm
SCAN_STEP = 1               # µm

scan_folder = Path("data") / "RasterScans" / datetime.now().strftime("scan_%Y-%m-%d_%H-%M-%S")
scan_folder.mkdir(parents=True, exist_ok=True)

profile_metadata = {
    "arm": ARM,
    "scan_axis": SCAN_AXIS,
    "scan_width": SCAN_WIDTH,
    "scan_step": SCAN_STEP,
    "profile_axis": PROFILE_AXIS,
    "profile_range": PROFILE_RANGE,
    "profile_speed": PROFILE_SPEED,
}

# ======================================================
# Inicialización
# ======================================================

# *** Crear el objeto System
suruga = System()

# *** Crear el objeto Profile
profile = Profile(suruga)

# *** Crear los objetos de AxisComponents el brazo izquierdo
x_axis = AxisComponents(suruga, SCAN_AXIS)
z_axis = AxisComponents(suruga, PROFILE_AXIS)

# *** Concectarse a la plataforma suruga
suruga.connect()

# Coordenada central en x del rectángulo de búsqueda
x_center = x_axis.get_actual_position()

# Definición de los pasos en x del rectángulo de búsqueda
x_positions = np.arange(
    x_center - SCAN_WIDTH / 2,
    x_center + SCAN_WIDTH / 2 + SCAN_STEP,
    SCAN_STEP,
)

# *** Definir las propiedades del profile en z
error = profile.set_profile(
    main_axis_number=PROFILE_AXIS,
    signal_ch1_number=1,
    main_range=PROFILE_RANGE,
    speed=PROFILE_SPEED,
    smoothing=0,
    accel_rate=100,
    decel_rate=100,
)

print(f"Error encontrado al momento de definir el profile: {error}")

# *** Definir la estructura que contiene los metadatos del escaneo y que funcionará como 
# header de metadata.json, este metadata es un diccionario mutable en el que se puede agregar
# información adicional a lo largo del programa.  

metadata = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "arm": ARM,
    "scan_axis": SCAN_AXIS,
    "profile_axis": PROFILE_AXIS,
    "step": SCAN_STEP,
    "width": SCAN_WIDTH,
    "profile_range": PROFILE_RANGE,
    "profile_speed": PROFILE_SPEED,
    "save_profile_txt": SAVE_PROFILE_TXT,
    "profiles": [],
}

# ======================================================
# Escaneo
# ======================================================

scan_data = [] 

for index, x_position in enumerate(x_positions):
    print(f"\n===== Profile {index} =====")

    # Mover el eje x a la posición de interés
    x_axis.move_absolute(float(x_position))
    x_axis.wait_until_complete()

    # Obtener la posicion central como referencia para la reconstrucción 
    # del plano en 2D
    x_actual = x_axis.get_actual_position()
    z_actual = z_axis.get_actual_position()
    print(f"Centro: X={x_actual:.3f} µm   Z={z_actual:.3f} µm")

    # Llevar a cabo el perfil
    profile.start()
    profile.wait_until_complete(intervalo=0.3)
    # Obtener la información del perfil
    data = profile.get_profile_data()
    # Limpiar los datos inválidos de la traza obtenida
    z_positions, signal = clean_profile_data(data)
    # Guardar en memoria 
    scan_data.append({"x": x_actual, "z_positions": z_positions, "signal": signal})

    filename = f"profile_{index:03d}.txt"
    if SAVE_PROFILE_TXT:
        save_profile_txt(scan_folder / filename, index, data, profile_metadata, x_actual, z_actual)

    metadata["profiles"].append(
        {
            "file": filename if SAVE_PROFILE_TXT else None,
            "center_x": x_actual,
            "center_z": z_actual,
            "samples": int(signal.size),
        }
    )

# ======================================================
# Construcción del mapa de calor
# ======================================================

heatmap_path = scan_folder / "heatmap.html"
max_power_position = create_heatmap(scan_data, heatmap_path)

# Incluyo esta información en el diccionario mutable
metadata["heatmap_file"] = heatmap_path.name
metadata["max_power_position"] = max_power_position

with (scan_folder / "metadata.json").open("w", encoding="utf-8") as file:
    json.dump(metadata, file, indent=4)

if MOVE_TO_MAX_POWER:
    print(
        "Moviendo al máximo de signal1: "
        f"X={max_power_position['x']:.3f} µm, Z={max_power_position['z']:.3f} µm"
    )
    x_axis.move_absolute(max_power_position["x"])
    x_axis.wait_until_complete()
    z_axis.move_absolute(max_power_position["z"])
    z_axis.wait_until_complete()
else:
    x_axis.move_absolute(x_center)
    x_axis.wait_until_complete()

print(f"\nEscaneo guardado en: {scan_folder}")
print(f"Mapa de calor: {heatmap_path}")
