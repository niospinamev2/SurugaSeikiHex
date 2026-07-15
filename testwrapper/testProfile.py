from pic_upv.suruga import *
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from pathlib import Path
from datetime import datetime
import numpy as np

suruga = System()

suruga.greet()

suruga.connect()

profile = Profile(suruga)

Test_axis = "y2"

error = profile.set_profile(
    main_axis_number=Test_axis,
    signal_ch1_number=1,
    main_range=50,
    speed=25,
    smoothing=0,
    accel_rate=100,
    decel_rate=100,
)

print(error)

print(profile.start())

estado = profile.wait_until_complete()

print("Estado final:", estado)

datos = profile.get_profile_data()


#=====================================================
# Saving the data to a file version 2
#=====================================================

data_folder = Path("profile_data")
data_folder.mkdir(exist_ok=True)

filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_" + Test_axis + "_att.txt"
filepath = data_folder / filename

matriz = np.column_stack([
    datos["main_position"],
    datos["sub1_position"],
    datos["sub2_position"],
    datos["signal1"],
    datos["signal2"],
])

np.savetxt(
    filepath,
    matriz,
    delimiter="\t",
    header="main_position\tsub1_position\tsub2_position\tsignal1\tsignal2",
    comments=""
)

# #=====================================================
# # Saving the data to a file version 1
# #=====================================================

# data_folder = Path("profile_data")
# data_folder.mkdir(exist_ok=True)

# filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_" + Test_axis + ".txt"
# filepath = data_folder / filename

# # header = [
# #     "main_position",
# #     "sub1_position",
# #     "sub2_position",
# #     "signal1",
# #     "signal2",
# # ]

# # with open(filepath, "w", encoding="utf-8") as f:
# #     f.write("\t".join(header) + "\n")

# header = list(datos.keys())

# with open(filepath, "w", encoding="utf-8") as f:
#     f.write("\t".join(header) + "\n")

# print(f"\nArchivo creado: {filepath}")

# with open(filepath, "a", encoding="utf-8") as f:
#     for fila in zip(
#         datos["main_position"],
#         datos["sub1_position"],
#         datos["sub2_position"],
#         datos["signal1"],
#         datos["signal2"],
#     ):
#         f.write("\t".join(map(str, fila)) + "\n")

#======================================================
# Plotting the results
#=====================================================


# w = datos["main_position"]
# p = datos["signal1"]
# fig = go.Figure(
#     data=[go.Scatter(x=w, y=p, mode="lines", name="Trace")]
# )
# fig.update_layout(
#     xaxis_title="Posición",
#     yaxis_title="Señal",
# )
# fig.show()

#======================================================
# Plotting the results
plt.figure(figsize=(10,5))

plt.plot(
    datos["main_position"],
    datos["signal1"]
)

plt.xlabel("Posición")
plt.ylabel("Señal")
plt.title("Resultado del Profile")
plt.grid(True)

plt.show()
