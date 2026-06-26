from pic_upv.control_suruga import *
import plotly.graph_objects as go
import numpy as np
import matplotlib.pyplot as plt


saludo()

SSM = cargar_suruga()

EQUIPO_DIRECCION = "5.113.249.131.1.1"
DISTANCIA_MAXIMA_SEGURA = 50000.0

align_system = SSM.System.Instance
align_system.SetAddress(EQUIPO_DIRECCION)

print("Direccion configurada:", EQUIPO_DIRECCION)
print("Version DLL:", align_system.DllVersion)


# ==========================================
# Rutina conexión 
esperar_conexion(align_system, timeout_s=20)


# ==========================================
# Rutina de profiling
alignment = SSM.Profile()

# Parametros para llevar a cabo un alineamiento Flat
param = SSM.Profile.ProfileParameter()

param.mainAxisNumber = 1
param.signalCh1Number = 1

param.mainRange = 100

param.speed = 30

param.accelRate = 100
param.decelRate = 100

param.smoothing = 0

# param.mainAxisNumber = 1
# param.signalCh1Number = 1
# param.mainRange = 500.0 # micras
# param.speed = 26.0 # micras/seg
# param.smoothing = 0 # microsegundos

error = alignment.SetProfile(param)
print(error)


# ==========================================================
# Iniciar profiling
# ==========================================================

error = alignment.Start()
print("Start:", error)


# ==========================================================
# Esperar a que termine
# ==========================================================

while True:

    status = alignment.GetProfileStatus()

    print("Estado:", status)

    if status != SSM.Profile.Status.Profiling:
        break

    time.sleep(0.1)

print("Estado final:", status)

# ==========================================================
# Número de paquetes
# ==========================================================

num_packets = alignment.GetProfilePacketSumIndex()

print("Número de paquetes:", num_packets)

# ==========================================================
# Descargar datos
# ==========================================================

main_position = []
sub1_position = []
sub2_position = []

signal1 = []
signal2 = []

for i in range(num_packets):

    print(f"Leyendo paquete {i}")

    data = alignment.RequestProfileData(i)

    main_position.extend(list(data.mainPositionList))
    sub1_position.extend(list(data.sub1PositionList))
    sub2_position.extend(list(data.sub2PositionList))

    signal1.extend(list(data.signalCh1List))
    signal2.extend(list(data.signalCh2List))

print()

print("Número de muestras:", len(main_position))

# ==========================================================
# Guardar datos en archivo
# ==========================================================

from datetime import datetime

# Fecha y hora de la adquisición
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Nombre del archivo
nombre_archivo = f"profile_{timestamp}.txt"

with open(nombre_archivo, "w") as f:
    f.write("main_position\tsignal1\tsub1_position\tsub2_position\tsignal2\n")

    for mp, s1, sp1, sp2, s2 in zip(
        main_position,
        signal1,
        sub1_position,
        sub2_position,
        signal2,
    ):
        f.write(f"{mp}\t{s1}\t{sp1}\t{sp2}\t{s2}\n")

print(f"Datos guardados en: {nombre_archivo}")

# ==========================================================
# Graficar
# ==========================================================


# def plot_profile(archivo):
#     """
#     Carga un archivo de perfil generado por Suruga y muestra la gráfica.

#     Parameters
#     ----------
#     archivo : str | Path
#         Ruta al archivo .txt generado durante la adquisición.
#     """

#     # Cargar datos (salta la primera línea con los encabezados)
#     data = np.loadtxt(archivo, skiprows=1)

#     main_position = data[:, 0]
#     signal1 = data[:, 1]

#     fig = go.Figure(
#         data=[
#             go.Scatter(
#                 x=main_position,
#                 y=signal1,
#                 mode="lines",
#                 name="Signal 1",
#             )
#         ]
#     )

#     fig.update_layout(
#         title=archivo,
#         xaxis_title="Posición",
#         yaxis_title="Señal",
#     )

#     fig.show()

# plot_profile(nombre_archivo)

data = np.loadtxt(nombre_archivo, skiprows=1)

main_position = data[:, 0]
signal1 = data[:, 1]


plt.figure(figsize=(10,5))

plt.plot(main_position, signal1)

plt.xlabel("Posición")
plt.ylabel("Señal")
plt.title("Resultado del Profile")

plt.grid(True)

plt.show()


