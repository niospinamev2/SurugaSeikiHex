from pic_upv.control_suruga_class import SurugaController

suruga = SurugaController()

suruga.saludo()

suruga.conectar()

pos = suruga.leer_posicion(1)

print(pos)

suruga.mover_eje(
    axis_number=1,
    distance=10000,
)

difpos = pos - suruga.leer_posicion(1)

print(difpos)