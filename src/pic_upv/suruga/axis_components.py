class AxisComponents:
    """Represents a single axis."""

    def __init__(self, system, axis_id: int):
        self.system = system
        self.axis_id = axis_id
        self.axis = system.SSM.AxisComponents(axis_id)

    def return_origin(self):
        self.axis.ReturnOrigin()
        print(f"[Axis {self.axis_id}] Return to origin.")

    # def move_absolute(self, position: float):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] MoveAbsolute({position})")

    # def move_relative(self, distance: float):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] MoveRelative({distance})")

    # def return_origin(self):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] ReturnOrigin()")
