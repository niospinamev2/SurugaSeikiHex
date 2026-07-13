"""
Test Automaper

⢸⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⡷⠀⠀
⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠢⣀⠀⠀
⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇ Are you winning son?
⢸⠀⠀⠀⠀ ⠖⠒⠒⠒⢤⠀⠀⠀⠀⠀⡇⠀⠀
⢸⠀⠀⣀⢤⣼⣀⡠⠤⠤⠼⠤⡄⠀⠀⡇⠀
⢸⠀⠀⠑⡤⠤⡒⠒⠒⡊⠙⡏⠀⢀⠀⡇⠀
⢸⠀⠀⠀⠇⠀⣀⣀⣀⣀⢀⠧⠟⠁⠀⡇
⢸⠀⠀⠀⠸⣀⠀⠀⠈⢉⠟⠓⠀⠀⠀⠀
⢸⠀⠀⠀⠀⠈⢱⡖⠋⠁⠀⠀⠀⠀⠀⠀⡇
⢸⠀⠀⠀⠀⣠⢺⠧⢄⣀⠀⠀⣀⣀⠀⠀⡇
⢸⠀⠀⠀⣠⠃⢸⠀⠀⠈⠉⡽⠿⠯⡆
⢸⠀⠀⣰⠁⠀⢸⠀⠀⠀⠀⠉⠉⠉⠀⠀⡇
⢸⠀⠀⠣⠀⠀⢸⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀
⢸⠀⠀⠀⠀⠀⢸⠀⢇⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀

This script tests the basic functionality of the AUTOMAPER module.

It loads a photonic chip layout from an Excel file, generates the
measurement plan, and computes the X-axis positions that would be
used by the Suruga positioning system.

No hardware movement is performed during this test. The purpose of
this script is solely to verify that the generated measurement plan
produces the expected positioning coordinates before executing any
real motion on the measurement platform.
"""

import pic_upv.automaper as automaper

EXCEL_FILE = "chipMaps/SurugaTest.xlsx"

chip, measurement_paths, measurement_plan = automaper.load_chip(
    EXCEL_FILE
)

origin_x1 = 0.0
origin_x2 = 0.0

for measurement in measurement_plan:

    x1_relative = -measurement["input"]["x"]

    x2_relative = -measurement["output"]["x"]

    abs_x1 = origin_x1 + x1_relative

    abs_x2 = origin_x2 + x2_relative

    print("\n" + "=" * 50)

    print(f"Device : {measurement['device']}")

    print(
        f"Input  : {measurement['input']['name']}"
    )

    print(
        f"Output : {measurement['output']['name']}"
    )

    print(
        f"Move X1 -> {abs_x1:.3f}"
    )

    print(
        f"Move X2 -> {abs_x2:.3f}"
    )

    input("Press Enter to continue...")