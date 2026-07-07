from pic_upv.suruga import *
import plotly.graph_objects as go
import matplotlib.pyplot as plt

suruga = System()

suruga.greet()

suruga.connect()

profile = Profile(suruga)

error = profile.set_profile(
    main_axis_number="x2",
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
