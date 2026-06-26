import time


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

    def configurar(
        self,
        main_axis=1,
        signal_ch1=1,
        rango=100,
        velocidad=26,
        smoothing=0,
        sub1_axis=0,
        sub2_axis=0,
        signal_ch2=0,
        accel=0,
        decel=0,
        sub1_range=0,
        sub2_range=0,
    ):

        param = self.system.SSM.Profile.ProfileParameter()

        param.mainAxisNumber = main_axis
        param.sub1AxisNumber = sub1_axis
        param.sub2AxisNumber = sub2_axis

        param.signalCh1Number = signal_ch1
        param.signalCh2Number = signal_ch2

        param.mainRange = rango
        param.sub1Range = sub1_range
        param.sub2Range = sub2_range

        param.speed = velocidad
        param.accelRate = accel
        param.decelRate = decel

        param.smoothing = smoothing

        return self.profile.SetProfile(param)

    # ======================================================
    # Inicio
    # ======================================================

    def iniciar(self):

        return self.profile.Start()

    # ======================================================
    # Esperar finalización
    # ======================================================

    def esperar(self, intervalo=0.1):

        while True:

            estado = self.profile.GetProfileStatus()

            print("Estado:", estado)

            if estado != self.system.SSM.Profile.Status.Profiling:
                return estado

            time.sleep(intervalo)

    # ======================================================
    # Descargar datos
    # ======================================================

    def obtener_datos(self):

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