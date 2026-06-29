from typing import Union
from pic_upv.suruga.axis_atribute import AxisAttribute
import time

class AxisComponents:
    """Represents a single axis."""

    def __init__(self, system, axis_id: Union[int, AxisAttribute, str]):
        # Originalmente era (self, system, axis_id: int)
        self.system = system
        self.attribute = AxisAttribute.from_any(axis_id)   # siempre AxisAttribute
        self.axis_id   = int(self.attribute)               # siempre int
        self.axis = system.SSM.AxisComponents(self.axis_id)

    #==================================================
    def get_actual_position(self):
        return self.axis.GetActualPosition()

    #==================================================
    def return_origin(self):
        self.axis.ReturnOrigin()
        print(f"[Axis {self.attribute.name} ({self.axis_id})] Return to origin.")

    #==================================================   
    def move_absolute(self, posicion):

        if not self.axis.IsServoOn():

            print("Activando servo...")

            self.axis.TurnOnServo()

            time.sleep(0.5)        

        return self.axis.MoveAbsolute(posicion)   

    #==================================================
    def move_relative(
        self,
        distance,
        speed = None,
    ):
        """
        Realiza un movimiento relativo.

        Parameters
        ----------
        distance : float
            Distancia del movimiento.

        speed : float, optional
            Velocidad máxima del movimiento.

            Si es None se conserva la velocidad
            previamente configurada.
        """

        if speed is not None:
            self.axis.SetMaxSpeed(speed)

        return self.axis.MoveRelative(distance)

    # def move_relative(self, distance: float):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] MoveRelative({distance})")

    # def move_absolute(self, position: float):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] MoveAbsolute({position})")

    # def move_relative(self, distance: float):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] MoveRelative({distance})")

    # def return_origin(self):
    #     self.system.ensure_connected()
    #     print(f"[Axis {self.axis_id}] ReturnOrigin()")


