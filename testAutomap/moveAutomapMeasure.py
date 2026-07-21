"""
Move Automap

"""
import time
import pic_upv.automaper as automaper
from pic_upv.suruga import System, AxisComponents, Alignment, PowerMeter
import os
import numpy as np

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
#-------------------------------------------------------
# Cargar el chip y el plan de medición desde el archivo 
# Excel
#-------------------------------------------------------

chip, measurement_paths, measurement_plan = automaper.load_chip(
    EXCEL_FILE
)

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

#-------------------------------------------------------
# Definir los parámetros de alineamiento para el brazo
# izquierdo y derecho
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

#-------------------------------------------------------
# Concectarse a la plataforma suruga
#------------------------------------------------------
suruga.connect()

#-------------------------------------------------------
# Crear el objeto PowerMeter
#-------------------------------------------------------
pm = PowerMeter(suruga)

# ======================================================
# Logica para definir el punto de origen del sistema, si 
# se va a usar el origen guardado o la posición actual,
# la posicion de inicio siempre deberá ser WG0
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

# ======================================================
# Rutina de medicion
# ======================================================

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

    #---------------------------------------------------
    # Mover el sistema a la posición absoluta calculada
    #---------------------------------------------------

    x1.move_absolute(abs_x1)
    x2.move_absolute(abs_x2)

    time.sleep(1)

    #---------------------------------------------------
    # Alinear el brazo izquierdo
    #---------------------------------------------------

    print("Aligning left arm ...")

    alignment.set_flat(**flat_left)
    alignment.start_flat()
    alignment.wait_until_complete()    

    time.sleep(1)

    #---------------------------------------------------
    # Alinear el brazo derecho
    #---------------------------------------------------

    print("Aligning right arm ...")

    alignment.set_flat(**flat_right)
    alignment.start_flat()
    alignment.wait_until_complete()    

    time.sleep(1)

    #---------------------------------------------------
    # Medir la potencia de salida
    #---------------------------------------------------  
     
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