import time
from typing import Union
from pic_upv.suruga.axis_atribute import AxisAttribute

class Alignment:
    """
    Maneja la funcionalidad de Alignment del controlador Suruga-Seiki.
    """

    def __init__(self, system):

        self.system = system
        self.alignment = system.SSM.Alignment()

    # ======================================================
    # Configuración Single
    # ======================================================

    def set_single(
        self,
        main_stage_x,
        sub_stage_x,
        pm_ch=1,
        analog_ch=0,
        search_range=100,
        field_threshold=0,
        peak_threshold=0,
        field_speed=10,
        peak_speed=5,
        smoothing=0,
        comparison_count=3,
        repeat_count=3,
        auto_range=True,
        init_range_setting=False,
        init_range=0,
        centroid_threshold=0,
        convergent_range=0,
        sub_angle=0,
        z_mode=None,
    ):

        param = self.system.SSM.Alignment.SingleParameter()

        param.mainStageNumberX = main_stage_x
        param.subStageNumberX = sub_stage_x

        param.pmCh = pm_ch
        param.analogCh = analog_ch

        param.searchRangeX = search_range

        param.fieldSearchThreshold = field_threshold
        param.peakSearchThreshold = peak_threshold

        param.fieldSearchSpeedX = field_speed
        param.peakSearchSpeedX = peak_speed

        param.smoothingRangeX = smoothing

        param.comparisonCount = comparison_count
        param.maxRepeatCount = repeat_count

        param.pmAutoRangeUpOn = auto_range
        param.pmInitRangeSettingOn = init_range_setting
        param.pmInitRange = init_range

        param.centroidThresholdX = centroid_threshold
        param.convergentRangeX = convergent_range

        param.subAngleX = sub_angle

        if z_mode is not None:
            param.zMode = z_mode

        return self.alignment.SetSingle(param)

    # ======================================================
    # Configuración Flat
    # ======================================================

    def set_flat(
        self,
        main_stage_x: Union[int, AxisAttribute, str],
        main_stage_y: Union[int, AxisAttribute, str],
        sub_stage_xy,
        pm_ch=1,
        analog_ch=1,
        search_range_x=50,
        search_range_y=20,
        field_threshold=0.2,
        peak_threshold=25,
        field_pitch_x=0.5,
        field_pitch_y=0.5,
        field_first_pitch_x=0,
        field_speed_x=200,
        field_speed_y=200,
        peak_speed_x=200,
        peak_speed_y=200,
        smoothing_x=40,
        smoothing_y=40,
        centroid_threshold_x=0,
        centroid_threshold_y=0,
        convergent_range_x=0.5,
        convergent_range_y=0.5,
        comparison_count=2,
        repeat_count=10,
        auto_range=True,
        init_range_setting=True,
        init_range=-40,
        sub_angle_x=0,
        sub_angle_y=0,
    ):

        param = self.system.SSM.Alignment.FlatParameter()

        # Numero del eje principal de alineamiento en X         
        param.mainStageNumberX = int(AxisAttribute.from_any(main_stage_x))

        # Numero del eje principal de alineamiento en Y 
        param.mainStageNumberY = int(AxisAttribute.from_any(main_stage_y))

        # Numero del eje de interpolacion XY po defecto 0 = None
        param.subStageNumberXY = sub_stage_xy

        param.subAngleX = sub_angle_x
        param.subAngleY = sub_angle_y

        param.pmCh = pm_ch
        param.analogCh = analog_ch

        param.pmAutoRangeUpOn = auto_range
        param.pmInitRangeSettingOn = init_range_setting
        param.pmInitRange = init_range

        param.fieldSearchThreshold = field_threshold
        param.peakSearchThreshold = peak_threshold

        param.searchRangeX = search_range_x
        param.searchRangeY = search_range_y

        param.fieldSearchPitchX = field_pitch_x
        param.fieldSearchPitchY = field_pitch_y
        param.fieldSearchFirstPitchX = field_first_pitch_x

        param.fieldSearchSpeedX = field_speed_x
        param.fieldSearchSpeedY = field_speed_y

        param.peakSearchSpeedX = peak_speed_x
        param.peakSearchSpeedY = peak_speed_y

        param.smoothingRangeX = smoothing_x
        param.smoothingRangeY = smoothing_y

        param.centroidThresholdX = centroid_threshold_x
        param.centroidThresholdY = centroid_threshold_y

        param.convergentRangeX = convergent_range_x
        param.convergentRangeY = convergent_range_y

        param.comparisonCount = comparison_count
        param.maxRepeatCount = repeat_count

        return self.alignment.SetFlat(param)

    # ======================================================
    # Inicio
    # ======================================================

    def start_single(self):
        return self.alignment.StartSingle()

    def start_flat(self):
        return self.alignment.StartFlat()

    # ======================================================
    # Control
    # ======================================================

    def stop(self):
        return self.alignment.Stop()

    def get_status(self):
        return self.alignment.GetStatus()

    def get_error_code(self):
        return self.alignment.GetErrorCode()

    def get_error_axis_id(self):
        return self.alignment.GetErrorAxisID()

    def get_aligning_status(self):
        return self.alignment.GetAligningStatus()

    # ======================================================
    # Espera
    # ======================================================

    def wait_until_complete(self, intervalo=0.1, retardo_inicial=0.2):

        time.sleep(retardo_inicial)

        while True:

            estado = self.get_status()

            print("Estado:", estado)

            if estado != self.system.SSM.Alignment.Status.Aligning:
                return estado

            time.sleep(intervalo)

    # ======================================================
    # Mediciones
    # ======================================================

    def get_voltage(self, canal):

        return self.alignment.GetVoltage(canal)

    def get_power(self, canal):

        return self.alignment.GetPower(canal)

    def get_measurement_wavelength(self, canal):

        return self.alignment.GetMeasurementWaveLength(canal)

    def set_measurement_wavelength(self, canal, longitud_onda):

        return self.alignment.SetMeasurementWaveLength(
            canal,
            longitud_onda,
        )

    # ======================================================
    # Descarga de perfiles
    # ======================================================

    def get_profile_data(self, profile_type):

        paquetes = self.alignment.GetProfilePacketSumIndex(profile_type)

        datos = {
            "main_position": [],
            "sub1_position": [],
            "sub2_position": [],
            "signal1": [],
            "signal2": [],
        }

        for i in range(paquetes):

            paquete = self.alignment.RequestProfileData(profile_type, i)

            datos["main_position"].extend(paquete.mainPositionList)
            datos["sub1_position"].extend(paquete.sub1PositionList)
            datos["sub2_position"].extend(paquete.sub2PositionList)

            datos["signal1"].extend(paquete.signalCh1List)
            datos["signal2"].extend(paquete.signalCh2List)

        return datos

    configurar_single = set_single
    configurar_flat = set_flat
    iniciar_single = start_single
    iniciar_flat = start_flat
    detener = stop
    estado = get_status
    codigo_error = get_error_code
    eje_error = get_error_axis_id
    estado_alineamiento = get_aligning_status
    esperar = wait_until_complete
    obtener_voltaje = get_voltage
    obtener_potencia = get_power
    obtener_longitud_onda = get_measurement_wavelength
    configurar_longitud_onda = set_measurement_wavelength
    obtener_datos = get_profile_data
