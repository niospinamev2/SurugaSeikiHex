# SurugaSeikiHex

**SurugaSeikiHex** is a Python wrapper for controlling the **Suruga-Seiki automated photonic alignment system** through the official `srgmc.dll` library using `pythonnet`.

The library provides a high-level interface to communicate with the motion controller, operate individual axes, execute alignment routines, acquire scan profiles, and interact with the integrated optical power meter.

The core implementation resides in the `pic_upv.suruga` package, while the `tests`, `testWrapper`, and `routines` directories contain practical examples intended for operation with real hardware.

## Setup

This project uses `uv` for dependency management and virtual environments.

1. Install uv (if you do not have it):
	- macOS/Linux: https://docs.astral.sh/uv/
	- Windows: https://docs.astral.sh/uv/

2. Create the virtual environment and install dependencies:

```bash
uv venv
uv sync
```

3. Activate the environment (optional if you use `uv run`):

```bash
source .venv/bin/activate
```

## Run

```bash
uv run python main.py
```

Before using the library, ensure that:

- Python 3.14 or newer is installed.
- .NET Runtime is available.
- The official TwinCAT XAE eXtended Automation Engineering software is installed.
- The required DLL files are present.
- The controller is reachable through the network.


## Features

- Motion controller connection and management
- Individual axis control
- Absolute and relative stage movements
- Automatic alignment routines

## Technologies

![Python](https://img.shields.io/badge/Python%203.14+-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![.NET](https://img.shields.io/badge/.NET%20CoreCLR-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)

## Dependencies

- `pythonnet>=3.1.0`
- `matplotlib>=3.10.8`
- `plotly>=6.0.0`
- `pyvisa-py>=0.8.1`
- `libusb-package>=1.0.26.3`
- `ipykernel` (for development notebooks)

Additionally, the official **Suruga-Seiki DLLs** and their .NET dependencies must be available inside:

```
src/pic_upv/dlls/
```

## Quick Start

```python
from pic_upv.suruga import System

suruga = System()

suruga.greet()

suruga.connect()
```

To connect to a controller using a different IP address, simply provide it when creating the System object.

```python
from pic_upv.suruga import System

suruga = System("192.168.1.20.1.1")

suruga.greet()

suruga.connect()
```

## Project Structure

```
SurugaSeikiHex/
│
├── src/
│   └── pic_upv/
│       └── suruga/
│           ├── system.py
│           ├── axis_components.py
│           ├── alignment.py
│           ├── profile.py
│           ├── power_meter.py
│           └── ...
│
├── tests/
│
├── testWrapper/
│
├── routines/
│
├── examples/
│
└── README.md
```
The project is organized into independent modules, each responsible for a specific subsystem of the Suruga-Seiki platform.

| Module | Description |
|---------|-------------|
| `System` | Controller connection and hardware management |
| `AxisComponents` | Motion control of individual axes |
| `Alignment` | Automatic alignment routines |
| `Profile` | Scan profile acquisition |
| `PowerMeter` | Optical power meter configuration and measurements |

> **📖 Documentation**
>
> For detailed installation instructions, API documentation, and usage examples, please visit the [project Wiki](https://github.com/niospinamev2/SurugaSeikiHex/wiki).
>
> For a complete guide to the Suruga-Seiki alignment workflow and operation, refer to the [Suruga Alignment Manual](https://github.com/niospinamev2/SurugaAlignmentManual).


