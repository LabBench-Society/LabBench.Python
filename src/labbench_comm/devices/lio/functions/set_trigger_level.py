from labbench_comm.devices.lio.definitions import ResponsePort
from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetTriggerLevel(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x32

    def __init__(self) -> None:
        super().__init__(request_length=3, response_length=0)
        self.level = 1

    @property
    def port(self) -> ResponsePort:
        return ResponsePort(self.request.get_byte(0))

    @port.setter
    def port(self, value: ResponsePort) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def level(self) -> int:
        return self.request.get_uint16(1)

    @level.setter
    def level(self, value: int) -> None:
        self.request.insert_uint16(1, value)

    def __str__(self) -> str:
        return "[0x32] Set Trigger Level"
