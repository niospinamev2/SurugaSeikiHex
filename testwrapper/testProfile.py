from pic_upv.suruga import *
import plotly.graph_objects as go
import matplotlib.pyplot as plt

suruga = System()

suruga.saludo()

suruga.conectar()

profile = Profile(suruga)

error = profile.configurar(
    main_axis="x2",
    signal_ch1=1,
    rango=500,
    velocidad=25,
    smoothing=0,
    accel = 100,
    decel = 100,
)

print(error)

print(profile.iniciar())

estado = profile.esperar()

print("Estado final:", estado)

datos = profile.obtener_datos()

#======================================================
# Plotting the results
#======================================================


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
#  
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