from labbench_comm.devices.lio.definitions import Logic, VoltageLevel
from labbench_comm.devices.lio.functions.base import _LIOFunction


class GetInterfaceStatus(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x50

    def __init__(self) -> None:
        super().__init__(request_length=0, response_length=4)

    @property
    def low_byte_level(self) -> VoltageLevel:
        return VoltageLevel(self.response.get_byte(0))

    @property
    def high_byte_level(self) -> VoltageLevel:
        return VoltageLevel(self.response.get_byte(1))

    @property
    def valid(self) -> bool:
        return self.response.get_bool(2)

    @property
    def logic(self) -> Logic:
        return Logic(self.response.get_byte(3))

    def __str__(self) -> str:
        return "[0x50] Get Interface Status"
