from labbench_comm.devices.lio.functions.base import _LIOFunction


class WriteSerialNumber(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x40

    def __init__(self) -> None:
        super().__init__(request_length=2, response_length=0)

    @property
    def serial_number(self) -> int:
        return self.request.get_uint16(0)

    @serial_number.setter
    def serial_number(self, value: int) -> None:
        self.request.insert_uint16(0, value)

    def __str__(self) -> str:
        return "[0x40] Write Serial Number"
