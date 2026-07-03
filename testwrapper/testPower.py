from pic_upv.suruga import System, PowerMeter

# Crear el sistema
suruga = System()

# Conectar con el controlador
suruga.conectar()

# Crear el objeto Power Meter
pm = PowerMeter(suruga)

# ======================================================
# Leer información del canal 1
# ======================================================

channel = 1

print(f"Canal: {channel}")

power = pm.get_power(channel)
print(f"Potencia: {power}")

range_value = pm.get_range(channel)
print(f"Rango: {range_value}")

wavelength = pm.get_wavelength(channel)
print(f"Longitud de onda: {wavelength}")