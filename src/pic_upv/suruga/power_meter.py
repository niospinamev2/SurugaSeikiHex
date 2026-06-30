class PowerMeter:
    """
    Handles the Power Meter functionality of the Suruga controller.
    """

    def __init__(self, system):

        self.system = system
        self.power_meter = system.SSM.PowerMeter()

    # ======================================================
    # Measurements
    # ======================================================

    def get_power(self, channel=1):

        return self.power_meter.GetPower(channel)

    def get_range(self, channel=1):

        return self.power_meter.GetRange(channel)

    def get_wavelength(self, channel=1):

        return self.power_meter.GetWavelength(channel)

    # ======================================================
    # Configuration
    # ======================================================

    def set_range(self, channel, range_value):

        return self.power_meter.SetRange(
            channel,
            range_value,
        )

    def set_wavelength(self, channel, wavelength):

        return self.power_meter.SetWaveLength(
            channel,
            wavelength,
        )

    # ======================================================
    # Communication
    # ======================================================

    def pause_communication(
        self,
        channel,
        enabled=True,
    ):

        return self.power_meter.PauseCommunication(
            channel,
            enabled,
        )