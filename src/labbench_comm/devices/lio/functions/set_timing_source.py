from labbench_comm.devices.lio.definitions import ResponsePort, TimingSource
from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetTimingSource(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x22

    def __init__(self) -> None:
        super().__init__(request_length=2, response_length=0)

    @property
    def port(self) -> ResponsePort:
        return ResponsePort(self.request.get_byte(0))

    @port.setter
    def port(self, value: ResponsePort) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def source(self) -> TimingSource:
        return TimingSource(self.request.get_byte(1))

    @source.setter
    def source(self, value: TimingSource) -> None:
        self.request.insert_byte(1, int(value))

    def __str__(self) -> str:
        return "[0x22] Set Timing Source"
