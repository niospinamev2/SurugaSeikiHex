from pathlib import Path
import sys
import pythonnet
import time

def obtener_ruta_dll():
    return Path(__file__).parent / "dlls" / "srgmc.dll"


def cargar_suruga():

    srgmc_path = obtener_ruta_dll()

    if not srgmc_path.exists():

        raise FileNotFoundError(
            f"No se encontró srgmc.dll en: {srgmc_path.parent}"
        )

    pythonnet.load("coreclr")

    import clr

    clr.AddReference(str(srgmc_path))

    import SurugaSeiki.Motion as SSM

    return SSM

def esperar_conexion(align_system, timeout_s):
    """
    Espera a que se establezca una conexion con el equipo Suruga-Seiki.

    Parameters
    ----------
    align_system : objeto
        Instancia de la clase "system" que contiene la propiedad
        "Connected".
    timeout_s : float
        Tiempo máximo de espera, en segundos.

    Returns
    -------
    bool
        "True" si la conexión se estableció antes de alcanzar el
        tiempo límite, "False" en caso contrario.
    """
    inicio = time.time()
    while not align_system.Connected and (time.time() - inicio) < timeout_s:
        print("Intentando conectar...", align_system.Connected)
        time.sleep(1)
    return align_system.Connected

def obtener_eje(align_system, axis_number):
    return align_system.AxisComponents(axis_number)


def saludo():
    print("Hola desde control_suruga.py")
