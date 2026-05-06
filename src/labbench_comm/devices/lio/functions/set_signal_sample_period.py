from labbench_comm.devices.lio.definitions import ResponsePort
from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetSignalSamplePeriod(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x24

    def __init__(self) -> None:
        super().__init__(request_length=3, response_length=0)
        self.period = 200

    @property
    def port(self) -> ResponsePort:
        return ResponsePort(self.request.get_byte(0))

    @port.setter
    def port(self, value: ResponsePort) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def period(self) -> int:
        return self.request.get_uint16(1)

    @period.setter
    def period(self, value: int) -> None:
        self.request.insert_uint16(1, value)

    def __str__(self) -> str:
        return "[0x24] Set Signal Sample Period"
