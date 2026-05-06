from labbench_comm.devices.lio.definitions import EventID
from labbench_comm.devices.lio.messages.base import _LIOMessage


class EventMessage(_LIOMessage):
    MESSAGE_LENGTH = 1

    @property
    def code(self) -> int:
        return 0x81

    @property
    def event(self) -> EventID:
        return EventID(self.packet.get_byte(0))

    @event.setter
    def event(self, value: EventID) -> None:
        self.packet.insert_byte(0, int(value))
