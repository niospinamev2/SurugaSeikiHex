from pathlib import Path
import time
import pythonnet

class SurugaController:

    def __init__(
        self,
        direccion="5.113.249.131.1.1",
        distancia_maxima_segura=50000.0,
    ):
        
        self.direccion = direccion
        self.distancia_maxima_segura = distancia_maxima_segura
        self.SSM = self._cargar_suruga()
        # Define una instancia de la clase "System"
        self.system = self.SSM.System.Instance
        # Le indica a la instancia de "System" la dirección del equipo Suruga-Seiki
        self.system.SetAddress(self.direccion)

    #==================================================    
    def _obtener_ruta_dll(self):

        return (
            Path(__file__).parent
            / "dlls"
            / "srgmc.dll"
        )
    
    #==================================================
    def _cargar_suruga(self):
        srgmc_path = self._obtener_ruta_dll()

        if not srgmc_path.exists():

            raise FileNotFoundError(
                f"No se encontró srgmc.dll en: {srgmc_path.parent}"
            )

        pythonnet.load("coreclr")

        import clr

        clr.AddReference(str(srgmc_path))

        import SurugaSeiki.Motion as SSM

        return SSM
    
    #==================================================
    def conectar(self, timeout_s=20):

        print("Conectando al equipo Suruga-Seiki...")
        print("Dirección:", self.direccion)
        print("Versión DLL:", self.system.DllVersion)

        inicio = time.time()

        while (
            not self.system.Connected
            and (time.time() - inicio) < timeout_s
        ):
        # Verificar que en efecto el sistema se encuentra conectado
            print(
                "Intentando conectar...",
                self.system.Connected, # Entrega True si el sistema está conectado, False si no lo está
            )

            time.sleep(1)

        return self.system.Connected
    
    #==================================================    
    def obtener_eje(self, axis_number):
        return self.SSM.AxisComponents(axis_number)

    def esperar_fin_movimiento(
        self,
        axis,
        timeout_s,
    ):

        inicio = time.time()

        while axis.IsMoving():

            if time.time() - inicio > timeout_s:

                axis.Stop()

                raise TimeoutError(
                    "El eje no terminó el movimiento a tiempo."
                )

            print(
                "Moviendo... posición:",
                axis.GetActualPosition(),
            )

            time.sleep(0.2)

    def mover_eje(
        self,
        axis_number,
        distance,
        max_speed=None,
        timeout_s=15,
    ):

        if abs(distance) > self.distancia_maxima_segura:

            raise ValueError(
                f"Distancia demasiado grande: {distance}"
            )

        if not self.conectar():

            raise ConnectionError(
                "No se pudo conectar."
            )

        if self.system.IsEmergencyAsserted():

            raise RuntimeError(
                "Emergencia activa."
            )

        # Es el equivalente a SSM.AxisComponents(axis_number) o SurugaSeiki.Motion.AxisComponents(axis_number)
        axis = self.obtener_eje(axis_number)

        print("Posición inicial:",
              axis.GetActualPosition())

        if axis.IsServoAlarm():

            raise RuntimeError(
                "El eje está en alarma."
            )

        if (
            axis.IsCwLimitSignalOn()
            or axis.IsCcwLimitSignalOn()
        ):

            raise RuntimeError(
                "El eje está en un límite."
            )

        if not axis.IsServoOn():

            print("Activando servo...")

            axis.TurnOnServo()

            time.sleep(0.5)

        if max_speed is not None:

            axis.SetMaxSpeed(max_speed)

        print(
            f"Moviendo eje {axis_number}"
        )

        axis.MoveRelative(distance)

        self.esperar_fin_movimiento(
            axis,
            timeout_s,
        )

        print(
            "Posición final:",
            axis.GetActualPosition(),
        )

    def leer_posicion(
        self,
        axis_number,
    ):

        axis = self.obtener_eje(
            axis_number
        )

        return axis.GetActualPosition()

    def saludo(self):

        print(
            "Hola desde SurugaController"
        )