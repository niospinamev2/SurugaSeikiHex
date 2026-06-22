from pathlib import Path
import sys
import pythonnet

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


def saludo():
    print("Hola desde control_suruga.py")
