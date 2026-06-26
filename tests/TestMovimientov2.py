from pic_upv.control_suruga import *

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

x1 = obtener_eje(align_system, 1)

x1.ReturnOrigin()