from pic_upv.suruga import *
import matplotlib.pyplot as plt

suruga = System()

suruga.conectar()

alignment = Alignment(suruga)

alignment.configurar_flat(
    main_stage_x="x1",
    main_stage_y="y1",
    sub_stage_xy=0,
)

alignment.iniciar_flat()

alignment.esperar()

# datos = alignment.obtener_datos(
#     suruga.SSM.Alignment.ProfileDataType.FieldSearch
# )

# # ======================================================
# # Plotear resultados
# # ======================================================

# plt.figure(figsize=(10,5))

# plt.plot(
#     datos["main_position"],
#     datos["signal1"]
# )

# plt.xlabel("Posición")
# plt.ylabel("Señal")
# plt.title("Resultado del Profile")
# plt.grid(True)

# plt.show()