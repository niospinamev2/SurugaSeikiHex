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
# Construir el mapa 2D
# =============================================================
# Cambio para que funcione sin importar desde que carpeta se ejecute el script
DATA_FOLDER = Path(__file__).resolve().parent

scan_folder = DATA_FOLDER / "scan_2026-08-03_13-58-34"

metadata_file = scan_folder / "metadata.json"

metadata = load_scan_metadata(metadata_file)

x_positions = []
profiles = []

# Utilizamos el primer perfil para definir el eje Z común
first_profile = scan_folder / metadata["profiles"][15]["file"]
z_common, _ = load_profile(first_profile)

for profile in metadata["profiles"]:

    profile_file = scan_folder / profile["file"]

    x_positions.append(profile["center_x"])

    z, signal = load_profile(profile_file)

    # Interpolar cada perfil sobre el mismo eje Z
    signal_interp = np.interp(z_common, z, signal)

    profiles.append(signal_interp)

print(x_positions)

heatmap = np.array(profiles)

print(heatmap.shape)
print(len(z_common))
print(len(x_positions))

fig = go.Figure()

fig.add_trace(
    go.Heatmap(
        x=z_common,
        y=x_positions,
        z=heatmap,
        colorscale="Viridis",
        colorbar_title="Signal 1 (V)",
    )
)

fig.update_layout(
    title="Raster scan",
    xaxis_title="Z position (µm)",
    yaxis_title="X position (µm)",
    template="plotly_white",
)

fig.write_html(
    scan_folder / "heatmap.html",
    include_plotlyjs="cdn",
)

fig.show()
