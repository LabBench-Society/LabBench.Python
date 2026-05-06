from labbench_comm.devices.lio.definitions import Logic, VoltageLevel
from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetInterfaceLogic(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x49

    def __init__(self) -> None:
        super().__init__(request_length=3, response_length=0)

    @property
    def low_byte_level(self) -> VoltageLevel:
        return VoltageLevel(self.request.get_byte(0))

    @low_byte_level.setter
    def low_byte_level(self, value: VoltageLevel) -> None:
        if value is VoltageLevel.Invalid:
            raise ValueError("Invalid value")
        self.request.insert_byte(0, int(value))

    @property
    def high_byte_level(self) -> VoltageLevel:
        return VoltageLevel(self.request.get_byte(1))

    @high_byte_level.setter
    def high_byte_level(self, value: VoltageLevel) -> None:
        if value is VoltageLevel.Invalid:
            raise ValueError("Invalid value")
        self.request.insert_byte(1, int(value))

    @property
    def logic(self) -> Logic:
        return Logic(self.request.get_byte(2))

    @logic.setter
    def logic(self, value: Logic) -> None:
        self.request.insert_byte(2, int(value))

    def __str__(self) -> str:
        return "[0x49] Set Interface Logic"
