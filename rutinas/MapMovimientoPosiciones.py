import pic_upv.automaper as automaper

EXCEL_FILE = "AUTOMAP/chip_layout.xlsx"

chip, measurement_plan = automaper.load_chip(EXCEL_FILE)

automaper.plot_chip(chip)
automaper.plot_measurement_plan(measurement_plan, chip)
