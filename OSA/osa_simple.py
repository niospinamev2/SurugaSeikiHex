import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pyvisa


# Esta clase actua como una caja que solo busca almacenar dos variables 
# Wavelength y Power, actua como una clase pasiva que recibe los resulta
# dos de la medición y lo almacena de forma organizada
@dataclass
class TraceData:
    wavelength_nm: np.ndarray
    power_dbm: np.ndarray

    def save_txt(self, path):
        # Convertir la ruta en un objeto Path
        path = Path(path)
        # Verifico la carpeta donde se encuentra el archivo, mkdir()
        # crea la carpeta en caso de que no exista, parents=True crea carpetas 
        # intermedias si hacen falta, exist_ok=True evita que aparezca un error 
        # si la carpeta ya existe
        path.parent.mkdir(parents=True, exist_ok=True)
        data = np.column_stack([self.wavelength_nm, self.power_dbm])
        np.savetxt(
            path,
            data,
            fmt="%.10f", # Escribe cada número con 10 decimales
            delimiter="\t", # Tab como separador
            header="Wavelength [nm]\tPower [dBm]",
        )


class SimpleVisaInstrument:
    def __init__(
        self,
        resource_address,
        timeout_ms=30000,
        read_termination="\n",
        write_termination="\n",
        visa_library=None,
        **resource_settings,
    ):
        self.resource_address = resource_address
        self.timeout_ms = timeout_ms
        self.read_termination = read_termination
        self.write_termination = write_termination
        self.visa_library = visa_library
        self.resource_settings = resource_settings
        self.rm = None
        self.inst = None

    def connect(self):
        if self.visa_library is None:
            self.rm = pyvisa.ResourceManager()
        else:
            self.rm = pyvisa.ResourceManager(self.visa_library)
        self.inst = self.rm.open_resource(self.resource_address)
        self.inst.timeout = self.timeout_ms
        self.inst.read_termination = self.read_termination
        self.inst.write_termination = self.write_termination
        for name, value in self.resource_settings.items():
            setattr(self.inst, name, value)
        return self

    def close(self):
        if self.inst is not None:
            self.inst.close()
            self.inst = None
        if self.rm is not None:
            self.rm.close()
            self.rm = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc, traceback):
        self.close()
        return False

    def write(self, command):
        self.inst.write(command)

    def query(self, command):
        return self.inst.query(command).strip()

    @property
    def idn(self):
        return self.query("*IDN?")

    def query_floats(self, command):
        response = self.query(command)
        return np.array([float(x) for x in response.split(",") if x.strip()])


class YeniOSA(SimpleVisaInstrument):
    """Minimal driver for the Yenista/EXFO OSA20 SCPI interface."""

    def __init__(self, resource_address="TCPIP0::192.168.54.1::5025::SOCKET", **kwargs):
        kwargs.setdefault("read_termination", "\r\n")
        kwargs.setdefault("write_termination", "\r\n")
        super().__init__(resource_address, **kwargs)

    def setup_sweep(
        self,
        center_nm=1565.0,
        span_nm=80.0,
        sensitivity_dbm=-70,
        resolution_nm=0.05,
        display=True,
    ):
        self.write(":OSA 1")
        self.write(f":DISPlay {1 if display else 0}")
        self.write(":UNIT:X 0")
        self.write(":UNIT:Y 0")
        self.write(":INITiate:SMODe 0")
        self.write(f":SENSe:WAVelength:CENTer {center_nm * 1e-9:g}")
        self.write(f":SENSe:WAVelength:SPAN {span_nm * 1e-9:g}")
        self.write(f":SENSe {sensitivity_dbm:g}")
        self.write(f":SENSe:BANDwidth {resolution_nm * 1e-9:g}")

    def run_sweep(
        self,
        trace=1,
        averages=1,
        timeout_s=120,
        start_delay_s=1.0,
        post_sweep_delay_s=10.0,
    ):
        self.write(f":TRACe{trace}:ACT")
        if averages > 1:
            self.write(f":TRACe{trace}:TYPE 3")
            self.write(f":TRACe{trace}:RAVG {averages}")
        else:
            self.write(f":TRACe{trace}:TYPE 1")

        self.write(":CLEar")
        self.write(":INITiate:IMMediate")
        print("Sweep started, waiting for completion...")
        time.sleep(start_delay_s)
        original_timeout = self.inst.timeout
        self.inst.timeout = max(original_timeout, int(timeout_s * 1000))
        try:
            self.query("*OPC?")
        except pyvisa.errors.VisaIOError as exc:
            raise TimeoutError(
                f"Yenista sweep did not finish within {timeout_s} seconds"
            ) from exc
        finally:
            self.inst.timeout = original_timeout
        print("Sweep progress: 100%")
        print(f"Waiting {post_sweep_delay_s:g} s before reading trace data...")
        time.sleep(post_sweep_delay_s)

    def get_trace(self, trace=1, read_timeout_s=120):
        print("Reading trace metadata...")
        start_m = float(self.query(f":TRACe{trace}:DATA:STAR?"))
        step_m = float(self.query(f":TRACe{trace}:DATA:SAMP?"))
        npoints = int(float(self.query(f":TRACe{trace}:DATA:LENG?")))
        print(f"Trace points reported by OSA: {npoints}")
        if npoints <= 0:
            raise RuntimeError("The OSA did not report any trace points.")

        print("Reading trace power data...")
        original_timeout = self.inst.timeout
        self.inst.timeout = max(original_timeout, int(read_timeout_s * 1000))
        try:
            power_dbm = self.query_floats(f":TRACe{trace}:DATA? ASC,DBM")
        finally:
            self.inst.timeout = original_timeout

        if len(power_dbm) != npoints:
            print(f"Warning: OSA reported {npoints} points but returned {len(power_dbm)}.")
        wavelength_nm = (start_m + step_m * np.arange(npoints)) * 1e9
        return TraceData(wavelength_nm=wavelength_nm[: len(power_dbm)], power_dbm=power_dbm)


class YokogawaOSA(SimpleVisaInstrument):
    """Minimal driver for a Yokogawa AQ6370-series OSA."""

    TRACE_NAMES = {
        1: "A",
        2: "B",
        3: "C",
        4: "D",
        5: "E",
        6: "F",
        7: "G",
    }

    def __init__(
        self,
        resource_address="TCPIP0::169.68.68.2::10001::SOCKET",
        username="anonymous",
        password="0123",
        **kwargs,
    ):
        super().__init__(resource_address, **kwargs)
        self.username = username
        self.password = password

    def connect(self):
        super().connect()
        if self.username and self.password:
            self.query(f'open "{self.username}","{self.password}"')
        return self

    def setup_sweep(
        self,
        center_nm=1565.0,
        span_nm=80.0,
        resolution_nm=0.02,
        points_auto=True,
        points=20001,
        sensitivity_command=None,
    ):
        self.write(":INITiate:SMODe 1")
        self.write(f":SENSe:WAVelength:CENTer {center_nm * 1e-9:g}")
        self.write(f":SENSe:WAVelength:SPAN {span_nm * 1e-9:g}")
        self.write(f":SENSe:BWIDth:RESolution {resolution_nm * 1e-9:g}")
        self.write(f":SENSe:SWEep:POINts:AUTO {1 if points_auto else 0}")
        if not points_auto:
            self.write(f":SENSe:SWEep:POINts {points}")
        if sensitivity_command:
            self.write(sensitivity_command)

    def run_sweep(self, trace=1, averages=1, poll_s=0.5):
        trace_name = self._trace_name(trace)
        self.write(f":TRACe:ACTive {trace}")
        self.write(f":TRACe:ATTRibute:TR{trace_name} 0")
        if averages > 1:
            self.write(f":TRACe:ATTRibute:RAVGTR{trace_name} {averages}")
        self.write("*CLS")
        self.write(":INITiate:IMMediate")
        self._wait_until_idle(poll_s=poll_s)

    def get_trace(self, trace=1):
        trace_name = self._trace_name(trace)
        wavelength_m = self.query_floats(f":TRACe:X? TR{trace_name}")
        power_dbm = self.query_floats(f":TRACe:Y? TR{trace_name}")
        return TraceData(wavelength_nm=wavelength_m * 1e9, power_dbm=power_dbm)

    def _wait_until_idle(self, poll_s):
        while True:
            status = int(float(self.query(":STATUS:OPERATION:CONDITION?")))
            if status == 1:
                print("Sweep progress: 100%")
                return
            print(f"Waiting, instrument status: {status}")
            time.sleep(poll_s)

    def _trace_name(self, trace):
        if isinstance(trace, str):
            return trace.upper().replace("TR", "")
        return self.TRACE_NAMES[int(trace)]


def create_osa(kind, resource_address=None, **kwargs):
    kind = kind.lower()
    if kind in {"yeni", "yenista", "exfo", "osa20"}:
        return YeniOSA(resource_address or "TCPIP0::192.168.54.1::5025::SOCKET", **kwargs)
    if kind in {"yoko", "yokogawa", "aq6370", "aq6370e"}:
        return YokogawaOSA(resource_address or "TCPIP0::169.68.68.2::10001::SOCKET", **kwargs)
    raise ValueError(f"Unknown OSA kind: {kind}")
