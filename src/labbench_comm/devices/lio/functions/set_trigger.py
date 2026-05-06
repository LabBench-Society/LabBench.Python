from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetTrigger(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x17

    def __init__(self) -> None:
        super().__init__(request_length=3, response_length=0)

    @property
    def trigger(self) -> bool:
        return (self.request.get_byte(0) & 0x01) != 0

    @trigger.setter
    def trigger(self, value: bool) -> None:
        bit_field = self.request.get_byte(0)
        bit_field = bit_field | 0x01 if value else bit_field & 0xFE
        self.request.insert_byte(0, bit_field)

    @property
    def stimulus_trigger(self) -> bool:
        return (self.request.get_byte(0) & 0x02) != 0

    @stimulus_trigger.setter
    def stimulus_trigger(self, value: bool) -> None:
        bit_field = self.request.get_byte(0)
        bit_field = bit_field | 0x02 if value else bit_field & 0xFD
        self.request.insert_byte(0, bit_field)

    @property
    def trigger_code(self) -> int:
        return self.request.get_uint16(1)

    @trigger_code.setter
    def trigger_code(self, value: int) -> None:
        self.request.insert_uint16(1, value)

    def __str__(self) -> str:
        return "[0x17] SetTrigger"
