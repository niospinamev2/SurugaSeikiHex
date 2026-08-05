"""
===============================================================================
Bla
===============================================================================

Purpose
-------
Llevar el escaneo de la potencia de salida de un puerto de un DUT, en la version
2 se busca facilitar la forma en la que se selecciona el brazo.

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
from pic_upv.suruga import System, AxisComponents, Profile, PowerMeter
import numpy as np
from pprint import pprint
from datetime import datetime
from pathlib import Path
import json


# ======================================================
# Configuración
# ======================================================

ARM = 1                     # 1 = brazo izquierdo | 2 = brazo derecho

SCAN_AXIS = f"x{ARM}"
PROFILE_AXIS = f"z{ARM}"

PROFILE_RANGE = 50          # µm
PROFILE_SPEED = 25          # µm/s

SCAN_WIDTH = 50             # µm
SCAN_STEP = 1               # µm


# ======================================================
# Carpeta del escaneo
# ======================================================

scan_folder = (
    Path("data") / "RasterScans" /  
    datetime.now().strftime("scan_%Y-%m-%d_%H-%M-%S")
)

# Para crear las carpetas intermedias si no existen  
scan_folder.mkdir(parents=True, exist_ok=True)

# ======================================================
# Inicialización
# ======================================================
# Inicialización de los equipos

# *** Crear el objeto System
suruga = System()

# *** Crear el objeto Profile
profile = Profile(suruga)

# *** Crear los objetos de AxisComponents el brazo izquierdo
x = AxisComponents(suruga, SCAN_AXIS)
z = AxisComponents(suruga, PROFILE_AXIS)

# *** Concectarse a la plataforma suruga
suruga.connect()

# Inicialización de los parametros de escaneo

# *** Definir la coordenada central y los pasos en x del 
# rectangulo de busqueda

x_center = x.get_actual_position()

x0 = x_center - SCAN_WIDTH / 2
x1 = x_center + SCAN_WIDTH / 2

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

# *** Definir la estructura que contiene los metadatos del escaneo

metadata = {
    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "arm": ARM,
    "scan_axis": SCAN_AXIS,
    "profile_axis": PROFILE_AXIS,
    "step": SCAN_STEP,
    "width": SCAN_WIDTH,
    "profiles": [],
}

# ======================================================
# Escaneo
# ======================================================

scan_data = []

for i, x_position in enumerate(np.arange(x0, x1 + SCAN_STEP, SCAN_STEP)):

    print(f"\n===== Profile {i} =====")

    # --------------------------------------------------
    # Mover eje X
    # --------------------------------------------------

    x.move_absolute(x_position)
    x.wait_until_complete()

    # Obtener la posicion central como referencia para la reconstrucción 
    # del plano en 2D
    x_actual = x.get_actual_position()
    z_actual = z.get_actual_position()

    print(f"Centro: X={x_actual:.3f} µm   Z={z_actual:.3f} µm")

    # --------------------------------------------------
    # Ejecutar profile
    # --------------------------------------------------

    profile.start()
    profile.wait_until_complete(intervalo=0.3)

    datos = profile.get_profile_data()

    # ----------------------------------------------
    # Guardar en memoria
    # ----------------------------------------------

    scan_data.append(
        {
            "x": x_actual,
            "z": z_actual,
            "profile": datos,
        }
    )

    # ----------------------------------------------
    # Guardar profile en TXT
    # ----------------------------------------------

    filename = f"profile_{i:03d}.txt"

    filepath = scan_folder / filename

    matriz = np.column_stack([
        datos["main_position"],
        datos["sub1_position"],
        datos["sub2_position"],
        datos["signal1"],
        datos["signal2"],
    ])

    # Definir un header mas descriptivo

    header = (
        f"Profile: {i:03d}\n"
        f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Center X: {x_actual:.3f} um\n"
        f"Center Z: {z_actual:.3f} um\n"
        f"Arm: {ARM}\n"
        f"Scan axis: {SCAN_AXIS}\n"
        f"Profile axis: {PROFILE_AXIS}\n"
        f"Profile range: {PROFILE_RANGE} um\n"
        f"Profile speed: {PROFILE_SPEED} um/s\n"
        "\n"
        "main_position\tsub1_position\tsub2_position\tsignal1\tsignal2"
    )

    np.savetxt(
        filepath,
        matriz,
        delimiter="\t",
        header=header,
        comments="# ", # Revisar luego para saber si los comentarios salen con numeral duplicado
    )

    # ----------------------------------------------
    # Actualizar metadata
    # ----------------------------------------------

    metadata["profiles"].append(
        {
            "file": filename,
            "center_x": x_actual,
            "center_z": z_actual,
        }
    )

# ======================================================
# Volver al centro
# ======================================================

x.move_absolute(x_center)
x.wait_until_complete()

# ======================================================
# Guardar metadata
# ======================================================

metadata_file = scan_folder / "metadata.json"

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=4)

print(f"\nEscaneo guardado en: {scan_folder}")







# # Info metadata

# metadata = {
#     "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#     "scan_axis": "x2",
#     "profile_axis": "z2",
#     "step": step,
#     "width": width,
#     "profiles": [],
# }









# scan_data = []

# for x in np.arange(x0, x1 + step, step):

#     x2.move_absolute(x)
#     estado = x2.wait_until_complete()
#     print(estado)   
#     print(f"Posición X2: {x2.get_actual_position()} µm")
#     print(profile.start())
#     estado = profile.wait_until_complete()
#     print("Estado final:", estado)

#     x_actual = x2.get_actual_position()
#     z_actual = z2.get_actual_position()
#     datos = profile.get_profile_data()

#     scan_data.append(
#         {
#             "x": x_actual,
#             "z": z_actual,
#             "profile": datos,
#         }
#     )

#     filename = f"profile_{i:03d}.txt"

#     metadata["profiles"].append(
#     {
#         "file": filename,
#         "center_x": x_actual,
#         "center_z": z_actual,
#     }
#     )

#     # Ejecutar profile en Z

# x2.move_absolute(x_center)

# json.dump(metadata, ...)









# for x in np.arange(x0, x1, step):

#     system.axis["x2"].move_absolute(x)

#     profile.set_profile(...)

#     profile.start()

#     profile.wait_until_complete()

#     datos = profile.get_profile_data()

#     profiles.append(datos["signal1"])