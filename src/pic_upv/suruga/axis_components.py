from typing import Union
from pic_upv.suruga.axis_atribute import AxisAttribute

class AxisComponents:
    """Represents a single axis."""

    def __init__(self, system, axis_id: Union[int, AxisAttribute, str]):
        # Originalmente era (self, system, axis_id: int)
        self.system = system
        self.attribute = AxisAttribute.from_any(axis_id)   # siempre AxisAttribute
        self.axis_id   = int(self.attribute)               # siempre int
        self.axis = system.SSM.AxisComponents(self.axis_id)

    def return_origin(self):
        self.axis.ReturnOrigin()
        print(f"[Axis {self.attribute.name} ({self.axis_id})] Return to origin.")

    # def move_absolute(self, position: float):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] MoveAbsolute({position})")

    # def move_relative(self, distance: float):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] MoveRelative({distance})")

    # def return_origin(self):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] ReturnOrigin()")


