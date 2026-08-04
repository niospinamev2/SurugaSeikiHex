import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import json
import plotly.graph_objects as go

# =============================================================
# Funciones
# =============================================================

def load_scan_metadata(metadata_file: Path) -> dict:
    with open(metadata_file) as f:
        return json.load(f)


def load_profile(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """
    Load a profile file and return the measured positions and signal values.

    The function ignores header lines starting with ``#``, removes the padding
    rows stored as zeros by the controller, and sorts the data by the main
    position before returning it.

    Parameters
    ----------
    path : Path
        Path to the profile data file.

    Returns
    -------
    tuple[np.ndarray, np.ndarray]
        A tuple containing:

        - The measured main positions.
        - The corresponding Signal 1 values.

    Examples
    --------
    Load a profile and plot the measured signal.

    >>> z, signal = load_profile(Path("profile_004.txt"))
    >>> plt.plot(z, signal)
    """

    data = np.loadtxt(path, comments="#")
    z = data[:, 0]       # main_position
    signal_1 = data[:, 3]  # signal1

    measured = (z != 0) & np.isfinite(z) & np.isfinite(signal_1)
    z, signal_1 = z[measured], signal_1[measured]

    # np.interp exige que la coordenada sea creciente.
    order = np.argsort(z)
    return z[order], signal_1[order]

# =============================================================
# Cargar información
# =============================================================
# Cambio para que funcione sin importar desde que carpeta se ejecute el script
DATA_FOLDER = Path(__file__).resolve().parent

scan_folder = DATA_FOLDER / "scan_2026-08-03_13-58-34"

metadata_file = scan_folder / "metadata.json"

metadata = load_scan_metadata(metadata_file)

for profile in metadata["profiles"]:

    profile_file = scan_folder / profile["file"]

    center_x = profile["center_x"]
    center_z = profile["center_z"]

    z, signal_1 = load_profile(profile_file)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=z,
            y=signal_1,
            mode="lines",
            name="Signal 1",
        )
    )

    fig.add_vline(
        x=center_z,
        line_width=2,
        line_dash="dash",
        line_color="red",
    )

    fig.update_layout(
        title=f"{profile_file.stem} measured at x = {center_x:.2f} µm",
        xaxis_title="Main Position (µm)",
        yaxis_title="Signal 1 (V)",
        template="plotly_white",
    )

    fig.write_html(
        scan_folder / f"{profile_file.stem}.html",
        include_plotlyjs="cdn",
    )