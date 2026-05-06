from labbench_comm.devices.lio.definitions import (
    ResponseDevice,
    ResponsePort,
    ResponseSubClass,
    from_fixed_point,
    saturate,
)
from labbench_comm.devices.lio.messages.base import _LIOMessage


class SignalMessage(_LIOMessage):
    MESSAGE_LENGTH = 21

    @property
    def code(self) -> int:
        return 0x90

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
    def signal(self) -> float:
        return self.packet.get_uint16(3)

    @property
    def a(self) -> float:
        return self.packet.get_int32(5) / 4096.0

    @property
    def b(self) -> float:
        return self.packet.get_int32(9) / 4096.0

    @property
    def range(self) -> float:
        return self.packet.get_uint16(13)

    @property
    def value(self) -> float:
        if self.range == 0:
            return 0.0
        return saturate(self.signal / self.range, 0.0, 1.0)

    @property
    def target(self) -> float:
        return from_fixed_point(self.packet.get_int16(15), 5)

    @property
    def high_limit(self) -> float:
        return from_fixed_point(self.packet.get_int16(17), 5)

    @property
    def low_limit(self) -> float:
        return from_fixed_point(self.packet.get_int16(19), 5)

    @property
    def voltage(self) -> float:
        return self.a * self.signal / 1023.0 + self.b
