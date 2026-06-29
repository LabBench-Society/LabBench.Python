from labbench_comm.devices.lio.definitions import ResponsePort
from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetIndicators(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x12

    def __init__(self) -> None:
        super().__init__(request_length=6, response_length=0)

    @property
    def port(self) -> ResponsePort:
        return ResponsePort(self.request.get_byte(0))

    @port.setter
    def port(self, value: ResponsePort) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def led_bitfield(self) -> int:
        return self.request.get_byte(1)

    @led_bitfield.setter
    def led_bitfield(self, value: int) -> None:
        self.request.insert_byte(1, value)

    @property
    def duration(self) -> int:
        return self.request.get_uint32(2)

    @duration.setter
    def duration(self, value: int) -> None:
        self.request.insert_uint32(2, value)

    def __str__(self) -> str:
        return "[0x12] Set Indicators"
