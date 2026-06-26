from pathlib import Path
import time
import pythonnet

class System:
    """Represents the DA1000 controller."""

    
    #==================================================
    def __init__(
        self,
        direccion="5.113.249.131.1.1",
    ):
        
        self.direccion = direccion
        self.SSM = self._cargar_suruga() # Ya es un atributo publico en System por lo que lo puedo llamar desde AxisComponents
        # Define una instancia de la clase "System"
        self.system = self.SSM.System.Instance
        # Le indica a la instancia de "System" la dirección del equipo Suruga-Seiki
        self.system.SetAddress(self.direccion)

    #==================================================    
    def _obtener_ruta_dll(self):

        return (
            Path(__file__).parent.parent
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
    def saludo(self):

        print(
            "Hola desde SurugaController"
        )


    # def __init__(self):
    #     self.connected = False
    #     self.address = None

    # def connect(self, address: str):
    #     self.address = address
    #     print(f"Connecting to {address}...")
    #     self.connected = True

    # def disconnect(self):
    #     print("Disconnecting...")
    #     self.connected = False

    # def ensure_connected(self):
    #     if not self.connected:
    #         raise RuntimeError("System is not connected.")
