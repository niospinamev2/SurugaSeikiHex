import time
from typing import Union
from pic_upv.suruga.axis_atribute import AxisAttribute

class Profile:
    """
    Maneja la funcionalidad de Profile del controlador Suruga.
    """

    def __init__(self, system):

        self.system = system
        self.profile = system.SSM.Profile()

    # ======================================================
    # Configuración
    # ======================================================

    def set_profile(
        self,
        main_axis_number: Union[int, AxisAttribute, str] = 1,
        signal_ch1_number=1,
        main_range=100,
        speed=26,
        smoothing=0,
        sub1_axis_number=0,
        sub2_axis_number=0,
        signal_ch2_number=0,
        accel_rate=0,
        decel_rate=0,
        sub1_range=0,
        sub2_range=0,
    ):

        param = self.system.SSM.Profile.ProfileParameter()

        param.mainAxisNumber = int(AxisAttribute.from_any(main_axis_number))
        param.sub1AxisNumber = sub1_axis_number
        param.sub2AxisNumber = sub2_axis_number

        param.signalCh1Number = signal_ch1_number
        param.signalCh2Number = signal_ch2_number

        param.mainRange = main_range
        param.sub1Range = sub1_range
        param.sub2Range = sub2_range

        param.speed = speed
        param.accelRate = accel_rate
        param.decelRate = decel_rate

        param.smoothing = smoothing

        return self.profile.SetProfile(param)

    # ======================================================
    # Inicio
    # ======================================================

    def start(self):

        return self.profile.Start()

    # ======================================================
    # Esperar finalización
    # ======================================================

    def wait_until_complete(self, intervalo=0.1, retardo_inicial=0.2):

        time.sleep(retardo_inicial)

        while True:

            estado = self.profile.GetProfileStatus()

            print("Estado:", estado)

            if estado != self.system.SSM.Profile.Status.Profiling:
                return estado

            time.sleep(intervalo)

    # ======================================================
    # Descargar datos
    # ======================================================

    def get_profile_data(self):

        paquetes = self.profile.GetProfilePacketSumIndex()

        print("Número de paquetes:", paquetes)

        datos = {
            "main_position": [],
            "sub1_position": [],
            "sub2_position": [],
            "signal1": [],
            "signal2": [],
        }

        for i in range(paquetes):

            paquete = self.profile.RequestProfileData(i)

            datos["main_position"].extend(paquete.mainPositionList)
            datos["sub1_position"].extend(paquete.sub1PositionList)
            datos["sub2_position"].extend(paquete.sub2PositionList)

            datos["signal1"].extend(paquete.signalCh1List)
            datos["signal2"].extend(paquete.signalCh2List)

        return datos

    configurar = set_profile
    iniciar = start
    esperar = wait_until_complete
    obtener_datos = get_profile_data
