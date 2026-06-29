from pic_upv.suruga import *

suruga = System()

suruga.conectar()

alignment = Alignment(suruga)

alignment.configurar_flat(
    main_stage_x=1,
    main_stage_y=2,
    sub_stage_xy=0,
)

alignment.iniciar_flat()

alignment.esperar()

# datos = alignment.obtener_datos(
#     suruga.SSM.Alignment.ProfileDataType.FieldSearch
# )