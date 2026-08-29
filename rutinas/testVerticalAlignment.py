# El objetivo de este script es verificar si puedo acceder a la salida 
# analógica del OPM

from pic_upv.suruga import System, AxisComponents, Alignment, PowerMeter
import matplotlib.pyplot as plt

suruga = System()

suruga.connect()

alignment = Alignment(suruga)

flat_left = {
    "main_stage_x": "x1",
    "main_stage_y": "z1",
    "sub_stage_xy": 0,
    "pm_ch": 1,
    "analog_ch": 1,
    "search_range_x": 500,
    "search_range_y": 500,
    "field_pitch_x": 100,
    "field_pitch_y": 100,
    "init_range": -30,
}

print(f"Voltaje inicial {alignment.get_voltage(1)}")

alignment.set_flat(**flat_left)
alignment.start_flat()
message = alignment.wait_until_complete()

print(f"El mensaje final es: {message}")

print(f"Voltaje final {alignment.get_voltage(1)}")


