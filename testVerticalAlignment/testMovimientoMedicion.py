from pic_upv.suruga import System, AxisComponents, Alignment, PowerMeter
import matplotlib.pyplot as plt
from pathlib import Path
import time

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


def guardar_origen(x1, x2, z1, z2):
    path = Path(ORIGIN_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        f.write(f"{x1}\n")
        f.write(f"{x2}\n")
        f.write(f"{z1}\n")
        f.write(f"{z2}\n")


def cargar_origen():

    with open(ORIGIN_FILE, "r") as f:
        x1 = float(f.readline())
        x2 = float(f.readline())
        z1 = float(f.readline())
        z2 = float(f.readline())

    return x1, x2, z1, z2


# ======================================================
# Configuración
# ======================================================

DEBUG_MODE = True             # True -> modo debug, False -> modo automático
USE_SAVED_ORIGIN = False      # True -> usar origen guardado
SAVE_ORIGIN = True            # Guardar el origen al iniciar


FILE_NAME = "originTest.txt"  # Nombre del archivo donde guardaremos las coordenadas de origen
ORIGIN_FILE = "data/origin/" + FILE_NAME

# Numero de veces que se repetirá la medición de todos los dispositivos
num_repeticiones = 1

# ======================================================
# Inicialización
# ======================================================






# # ======================================================
# # Posiciones del chip relativas al origen
# # ======================================================

# waveguides = [
#     {"name": "WG0", "x1":   0.0,   "x2":   0.0},
#     {"name": "WG1", "x1": -63.5,   "x2": -63.5},
#     {"name": "WG2", "x1": -127.0,  "x2": -127.0},
#     {"name": "WG3", "x1": -190.5,  "x2": -190.5},
# ]

# # ======================================================
# # Logica para definir el punto de origen del sistema, si 
# # se va a usar el origen guardado o la posición actual,
# # la posicion de inicio siempre deberá ser WG0
# # ======================================================

# if USE_SAVED_ORIGIN and os.path.exists(ORIGIN_FILE):

#     print("Usando origen almacenado...")

#     origin_x1, origin_x2 = cargar_origen()

#     x1.move_absolute(origin_x1)
#     x2.move_absolute(origin_x2)

# else:

#     print("Usando posición actual como origen...")

#     origin_x1 = x1.get_actual_position()
#     origin_x2 = x2.get_actual_position()

#     if SAVE_ORIGIN:
#         guardar_origen(origin_x1, origin_x2)
        
# print("Origen de la máquina")
# print(f"X1 = {origin_x1:.3f}")
# print(f"X2 = {origin_x2:.3f}")




