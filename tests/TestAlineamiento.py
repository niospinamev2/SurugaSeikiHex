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


# ==========================================
# Rutina alineamiento Flat
alignment = SSM.Alignment()

# Parametros para llevar a cabo un alineamiento Flat
param = SSM.Alignment.FlatParameter()

param.mainStageNumberX = 1
param.mainStageNumberY = 2

param.pmCh = 1

param.searchRangeX = 1000
param.searchRangeY = 1000

param.fieldSearchPitchX = 20
param.fieldSearchPitchY = 20

param.fieldSearchSpeedX = 100
param.fieldSearchSpeedY = 100

param.peakSearchSpeedX = 50
param.peakSearchSpeedY = 50

param.maxRepeatCount = 10

# Cargar la configuración de alineamiento Flat en el equipo Suruga-Seiki

error = alignment.SetFlat(param)
print(error)

error = alignment.StartFlat()
print(error)





