# import os

# print("Directorio de trabajo:")
# print(os.getcwd())

# print()

# print("Archivos que Python ve:")

# print(os.listdir())


from pprint import pprint
# from automaper import load_chip
import automaper


EXCEL_FILE = "AUTOMAP/chip_layout.xlsx"

# chip, measurement_plan = load_chip(EXCEL_FILE)

# pprint(chip)

# print()

# pprint(measurement_plan)

chip, measurement_paths = automaper.load_chip(EXCEL_FILE)

automaper.plot_chip(chip)
automaper.plot_measurement_paths(measurement_paths, chip)

print("=" * 80)
print("MEASUREMENT PLAN")
print("=" * 80)

for measurement in measurement_paths:

    # --------------------------------------------------
    # Buscar el dispositivo
    # --------------------------------------------------

    device = chip[measurement["device"]]

    # --------------------------------------------------
    # ¿El dispositivo está habilitado?
    # --------------------------------------------------

    if not device["measure"]:
        continue

    # --------------------------------------------------
    # ¿La combinación de puertos está habilitada?
    # --------------------------------------------------

    if not measurement["enabled"]:
        continue

    # --------------------------------------------------
    # Obtener los puertos
    # --------------------------------------------------

    input_port = device["ports"][measurement["input"]]

    output_port = device["ports"][measurement["output"]]

    print("=" * 50)

    print(f"Device : {measurement['device']}")
    print(f"Input  : {measurement['input']}")
    print(f"Output : {measurement['output']}")

    print(
        f"Move left fiber  -> "
        f"({input_port['x']}, {input_port['y']})"
    )

    print(
        f"Move right fiber -> "
        f"({output_port['x']}, {output_port['y']})"
    )

    # --------------------------------------------------
    # Measurement routine
    # --------------------------------------------------

