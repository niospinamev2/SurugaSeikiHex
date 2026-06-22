# from pic_upv.control_suruga import saludo
from pic_upv.control_suruga import *
import time

saludo()

SSM = cargar_suruga()

EQUIPO_DIRECCION = "5.113.249.131.1.1"
DISTANCIA_MAXIMA_SEGURA = 50000.0

def esperar_conexion(align_system, timeout_s):
    """
    Espera a que se establezca una conexion con el equipo Suruga-Seiki.

    Parameters
    ----------
    align_system : objeto
        Instancia de la clase "system" que contiene la propiedad
        "Connected".
    timeout_s : float
        Tiempo máximo de espera, en segundos.

    Returns
    -------
    bool
        "True" si la conexión se estableció antes de alcanzar el
        tiempo límite, "False" en caso contrario.
    """
    inicio = time.time()
    while not align_system.Connected and (time.time() - inicio) < timeout_s:
        print("Intentando conectar...", align_system.Connected)
        time.sleep(1)
    return align_system.Connected


def esperar_fin_movimiento(axis, timeout_s):
    """
    Espera a que un eje motorizado finalice su movimiento.

    Parameters
    ----------
    axis : objeto
        Instancia de la clase "AxisComponents" que contiene los metodos
        "IsMoving()", "Stop()", y "GetActualPosition()".
    timeout_s : float
        Tiempo máximo de espera, en segundos.

    Returns
    -------
    bool
        None.

    Exceptions
    -----------
    TimeoutError
        Se produce cuando el eje no finaliza el movimiento dentro
        del tiempo especificado.
    """
    inicio = time.time()
    while axis.IsMoving():
        if time.time() - inicio > timeout_s:
            axis.Stop()
            raise TimeoutError("El eje no termino el movimiento a tiempo. Se envio Stop().")
        print("Moviendo... posicion actual:", axis.GetActualPosition())
        time.sleep(0.2)


def mover_eje(axis_number, distance, max_speed, timeout_s):

    # Verificar que la distancia de movimiento no exceda el límite de seguridad
    if abs(distance) > DISTANCIA_MAXIMA_SEGURA:
        raise ValueError(
            f"Distancia demasiado grande para este script: {distance}. "
            f"Maximo permitido: +/-{DISTANCIA_MAXIMA_SEGURA}."
        )

    # Obtener la instancia del sistema y configurar la dirección del equipo
    print("Conectando al equipo Suruga-Seiki...")
    align_system = SSM.System.Instance
    align_system.SetAddress(EQUIPO_DIRECCION)

    print("Direccion configurada:", EQUIPO_DIRECCION)
    print("Version DLL:", align_system.DllVersion)

    # Esperar a que la conexión se establezca
    if not esperar_conexion(align_system, timeout_s=20):
        print("No se pudo conectar.")
        print("Error actual:", align_system.GetCurrentErrorCode())
        return 1

    # Verificar que no exista una condición de emergencia activa
    if align_system.IsEmergencyAsserted():
        print("Emergencia activa. No se movera ningun eje.")
        return 1
    
    # Crear el objeto asociado al eje seleccionado y mostrar su estado actual

    axis = SSM.AxisComponents(axis_number)

    print("Eje:", axis_number)
    print("Estado inicial:", axis.GetStatus())
    print("Error inicial:", axis.GetErrorCode())
    print("Servo on:", axis.IsServoOn())
    print("Posicion inicial:", axis.GetActualPosition())

    # Verificar que el eje no presente alarmas ni se encuentre en un 
    # límite mecánico  

    if axis.IsServoAlarm():
        print("El eje esta en alarma de servo. Revisa el equipo antes de mover.")
        return 1

    if axis.IsCwLimitSignalOn() or axis.IsCcwLimitSignalOn():
        print("El eje esta en limite. No se movera con este script.")
        return 1

    # Activar el servo si todavíá no está activado

    if not axis.IsServoOn():
        print("Activando servo...")
        error = axis.TurnOnServo()
        print("TurnOnServo:", error)
        time.sleep(0.5)

    # Configurar la veloxidad máxima en caso de ser especificada
    if max_speed is not None:
        print("Configurando velocidad maxima:", max_speed)
        print("SetMaxSpeed:", axis.SetMaxSpeed(max_speed))

    # Llevar a cabo el movimiento solicitado
    print(f"Moviendo eje {axis_number} de forma relativa: {distance}")
    error = axis.MoveRelative(distance)
    print("MoveRelative:", error)

    # Esperar a que el movimiento finalice o se alcance el tiempo límite
    esperar_fin_movimiento(axis, timeout_s=timeout_s)

    # Mostrar el estado final del eje  
    print("Estado final:", axis.GetStatus())
    print("Error final:", axis.GetErrorCode())
    print("Posicion final:", axis.GetActualPosition())
    return 0


# mover_eje(1, 30000, None, 15.0)

mover_eje(
    axis_number=1,
    distance=30000,
    max_speed=None,
    timeout_s=15.0
)