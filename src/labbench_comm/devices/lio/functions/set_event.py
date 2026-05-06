from datetime import date

from labbench_comm.devices.lio.definitions import DeviceEventType
from labbench_comm.devices.lio.functions.base import (
    EVENT_RECORD_SIZE,
    EVENT_TEXT_SIZE,
    _LIOFunction,
)


class SetEvent(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x47

    def __init__(self) -> None:
        super().__init__(request_length=EVENT_RECORD_SIZE + 1, response_length=0)
        self.date = date.today()
        self.event_id = 1
        self.valid = True
        self.text = ""

    @property
    def device_event(self) -> DeviceEventType:
        return DeviceEventType(self.request.get_byte(0))

    @device_event.setter
    def device_event(self, value: DeviceEventType) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def valid(self) -> bool:
        return self.request.get_byte(1) != 0

    @valid.setter
    def valid(self, value: bool) -> None:
        self.request.insert_byte(1, 1 if value else 0)

    @property
    def event_id(self) -> int:
        return self.request.get_uint32(2)

    @event_id.setter
    def event_id(self, value: int) -> None:
        self.request.insert_uint32(2, value)

    @property
    def date(self) -> date:
        return date(
            self.request.get_uint16(6),
            self.request.get_byte(8),
            self.request.get_byte(9),
        )

    @date.setter
    def date(self, value: date) -> None:
        self.request.insert_uint16(6, value.year)
        self.request.insert_byte(8, value.month)
        self.request.insert_byte(9, value.day)

    @property
    def text(self) -> str:
        return self.request.get_string(10, EVENT_TEXT_SIZE)

    @text.setter
    def text(self, value: str) -> None:
        self.request.insert_string(10, EVENT_TEXT_SIZE, value)

    def __str__(self) -> str:
        return "[0x47] Set Event"
