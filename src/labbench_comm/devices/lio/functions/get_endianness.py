from labbench_comm.devices.lio.functions.base import _LIOFunction


class GetEndianness(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x03

    def __init__(self) -> None:
        super().__init__(request_length=0, response_length=2)

    @property
    def endian_marker(self) -> int:
        return self.response.get_uint16(0)

    def __str__(self) -> str:
        return "[0x03] Get Endianness"
