
from pathlib import Path
from pprint import pprint

# -------------------------------------------------
# First choose one of the following imports
# Option 1 (recommended): Import the installed version from the pic_upv package.
from pic_upv import automaper
# Option 2: Import this version if you are editing the local osa_simple.py file and want to test those changes.
#import automaper
# -------------------------------------------------


# __file__ contains the rute of the current python file at execution
# Path creates an object Path that represents the route obtained with Path
# Resolve gives an absolute route of the path
# Parent gives the folder asociated with the route [1] goes up two levels from the file
# being the first level [0].

PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXCEL_FILE = PROJECT_ROOT / "chipMaps" / "SurugaTest.xlsx"

COUPLING = "Edge"


chip, measurement_paths, measurement_plan = automaper.load_chip(
    EXCEL_FILE,
    coupling=COUPLING,
)

automaper.plot_chip(chip)
automaper.plot_measurement_paths(measurement_paths, chip)
automaper.plot_measurement_plan(measurement_plan)

print("=" * 80)
print("PLAN COMPLETO (estructura de Python)")
print("=" * 80)
pprint(measurement_plan)

print()
print(f"Número de medidas que pasan el filtro: {len(measurement_plan)}")
