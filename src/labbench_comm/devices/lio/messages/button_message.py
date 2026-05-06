from labbench_comm.devices.lio.definitions import (
    ResponseDevice,
    ResponsePort,
    ResponseSubClass,
)
from labbench_comm.devices.lio.messages.base import _LIOMessage


class ButtonMessage(_LIOMessage):
    MESSAGE_LENGTH = 10

    @property
    def code(self) -> int:
        return 0x91

    @property
    def port(self) -> ResponsePort:
        return ResponsePort(self.packet.get_byte(0))

    @property
    def device(self) -> ResponseDevice:
        return ResponseDevice(self.packet.get_byte(1))

    @property
    def sub_class(self) -> ResponseSubClass:
        return ResponseSubClass(self.packet.get_byte(2))

    @property
    def button(self) -> int:
        return self.packet.get_byte(3)

    @property
    def state(self) -> bool:
        return self.packet.get_bool(4)

    @property
    def time(self) -> int:
        divisor = self.packet.get_byte(5)
        if divisor == 0:
            return 0
        return int(self.packet.get_uint32(6) / divisor)
