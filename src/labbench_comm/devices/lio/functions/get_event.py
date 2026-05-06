from datetime import date

from labbench_comm.devices.lio.definitions import DeviceEventType
from labbench_comm.devices.lio.functions.base import (
    EVENT_RECORD_SIZE,
    EVENT_TEXT_SIZE,
    _LIOFunction,
)


class GetEvent(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x46

    def __init__(self) -> None:
        super().__init__(request_length=1, response_length=EVENT_RECORD_SIZE)
        self.device_event = DeviceEventType.CALIBRATION_EVENT
        self.date = date.today()

    @property
    def device_event(self) -> DeviceEventType:
        return DeviceEventType(self.request.get_byte(0))

    @device_event.setter
    def device_event(self, value: DeviceEventType) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def valid(self) -> bool:
        return self.response.get_byte(0) != 0

    @valid.setter
    def valid(self, value: bool) -> None:
        self.response.insert_byte(0, 1 if value else 0)

    @property
    def event_id(self) -> int:
        return self.response.get_uint32(1)

    @event_id.setter
    def event_id(self, value: int) -> None:
        self.response.insert_uint32(1, value)

    @property
    def date(self) -> date:
        return date(
            self.response.get_uint16(5),
            self.response.get_byte(7),
            self.response.get_byte(8),
        )

    @date.setter
    def date(self, value: date) -> None:
        self.response.insert_uint16(5, value.year)
        self.response.insert_byte(7, value.month)
        self.response.insert_byte(8, value.day)

    @property
    def text(self) -> str:
        return self.response.get_string(9, EVENT_TEXT_SIZE)

    @text.setter
    def text(self, value: str) -> None:
        self.response.insert_string(9, EVENT_TEXT_SIZE, value)

    def __str__(self) -> str:
        return "[0x46] Get Event"
