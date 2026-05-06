from labbench_comm.devices.lio.definitions import (
    UINT16_MAX,
    InputTriggerSource,
    UpdateRate,
    saturate,
)
from labbench_comm.devices.lio.functions.base import _LIOFunction


class Start(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x16

    def __init__(self) -> None:
        super().__init__(request_length=8, response_length=0)
        self.trigger = InputTriggerSource.TRIG_NONE
        self.rate = UpdateRate.CLK20000Hz
        self.reset_on_completion = False
        self.restart_on_completion = False
        self.trigger_sequence_repeat = 1
        self.stimulus_program_repeat = 1

    @property
    def trigger(self) -> InputTriggerSource:
        return InputTriggerSource(self.request.get_byte(0))

    @trigger.setter
    def trigger(self, value: InputTriggerSource) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def rate(self) -> UpdateRate:
        return UpdateRate(self.request.get_byte(1))

    @rate.setter
    def rate(self, value: UpdateRate) -> None:
        self.request.insert_byte(1, int(value))

    @property
    def reset_on_completion(self) -> bool:
        return self.request.get_bool(2)

    @reset_on_completion.setter
    def reset_on_completion(self, value: bool) -> None:
        self.request.insert_bool(2, value)

    @property
    def restart_on_completion(self) -> bool:
        return self.request.get_bool(3)

    @restart_on_completion.setter
    def restart_on_completion(self, value: bool) -> None:
        self.request.insert_bool(3, value)

    @property
    def trigger_sequence_repeat(self) -> int:
        return self.request.get_uint16(4)

    @trigger_sequence_repeat.setter
    def trigger_sequence_repeat(self, value: int) -> None:
        self.request.insert_uint16(4, int(saturate(value, 0, UINT16_MAX)))

    @property
    def stimulus_program_repeat(self) -> int:
        return self.request.get_uint16(6)

    @stimulus_program_repeat.setter
    def stimulus_program_repeat(self, value: int) -> None:
        self.request.insert_uint16(6, int(saturate(value, 0, UINT16_MAX)))

    def __str__(self) -> str:
        return "[0x16] Start"
