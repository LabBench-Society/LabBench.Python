from labbench_comm.devices.lio.definitions import (
    DeviceState,
    ResponseDevice,
    ResponseSubClass,
    SystemError,
)
from labbench_comm.devices.lio.messages.base import _LIOMessage


class StatusMessage(_LIOMessage):
    MESSAGE_LENGTH = 7

    @property
    def code(self) -> int:
        return 0x80

    @property
    def state(self) -> DeviceState:
        return DeviceState(self.packet.get_byte(0))

    @property
    def port01(self) -> ResponseDevice:
        return ResponseDevice(self.packet.get_byte(1))

    @property
    def port01_subclass(self) -> ResponseSubClass:
        return ResponseSubClass(self.packet.get_byte(2))

    @property
    def port02(self) -> ResponseDevice:
        return ResponseDevice(self.packet.get_byte(3))

    @property
    def port02_subclass(self) -> ResponseSubClass:
        return ResponseSubClass(self.packet.get_byte(4))

    @property
    def power(self) -> bool:
        return self.packet.get_byte(5) != 0

    @property
    def error(self) -> SystemError:
        return SystemError(self.packet.get_byte(6))
