from labbench_comm.devices.lio.definitions import saturate
from labbench_comm.devices.lio.messages.base import _LIOMessage


class AnalogInputMessage(_LIOMessage):
    MESSAGE_LENGTH = 13

    @property
    def code(self) -> int:
        return 0x94

    @property
    def pin(self) -> int:
        return self.packet.get_byte(0)

    @property
    def signal(self) -> float:
        return self.packet.get_uint16(1)

    @property
    def a(self) -> float:
        return self.packet.get_int32(3) / 4096.0

    @property
    def b(self) -> float:
        return self.packet.get_int32(7) / 4096.0

    @property
    def range(self) -> float:
        return self.packet.get_uint16(11)

    @property
    def value(self) -> float:
        if self.range == 0:
            return 0.0
        return saturate(self.signal / self.range, 0.0, 1.0)

    @property
    def voltage(self) -> float:
        return self.a * self.signal / 1023.0 + self.b
