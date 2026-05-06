from labbench_comm.devices.lio.definitions import AnalogChannel
from labbench_comm.devices.lio.functions.base import _LIOFunction


class GetAnalogSignal(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x25

    def __init__(self) -> None:
        super().__init__(request_length=1, response_length=2)

    @property
    def channel(self) -> AnalogChannel:
        return AnalogChannel(self.request.get_byte(0))

    @channel.setter
    def channel(self, value: AnalogChannel) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def value(self) -> int:
        return self.response.get_uint16(0)

    @value.setter
    def value(self, value: int) -> None:
        self.response.insert_uint16(0, value)

    def __str__(self) -> str:
        return "[0x25] Get Analog Signal"
