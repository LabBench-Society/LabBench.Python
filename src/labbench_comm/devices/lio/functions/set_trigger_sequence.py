from labbench_comm.protocols.packet import ChecksumAlgorithmType, Packet

from labbench_comm.devices.lio.definitions import (
    UINT16_MAX,
    TriggerInstruction,
    UpdateRate,
    saturate,
)
from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetTriggerSequence(_LIOFunction):
    TRIGGER_SIZE = 5
    TRIGGER_SEQUENCE_LENGTH = 128

    @property
    def code(self) -> int:
        return 0x14

    def __init__(self) -> None:
        super().__init__(request_length=0, response_length=0)
        self.rate = UpdateRate.CLK20000Hz
        self.triggers: list[TriggerInstruction] = []

    def add(self, instruction: TriggerInstruction, duration: float | None = None) -> None:
        if duration is not None:
            instruction.duration = duration
        self.triggers.append(instruction)

    @staticmethod
    def encode_triggers(trigger: TriggerInstruction) -> int:
        value = 0
        value |= 0x01 if trigger.trigger_out else 0x00
        value |= 0x02 if trigger.stimulus_trigger_out else 0x00
        return value

    @property
    def number_of_instructions(self) -> int:
        return min(len(self.triggers), self.TRIGGER_SEQUENCE_LENGTH)

    def on_send(self) -> None:
        self.set_request(Packet(
            self.code,
            self.TRIGGER_SIZE * self.number_of_instructions,
            ChecksumAlgorithmType.CRC8CCITT,
        ))

        address = 0
        for trigger in self.triggers[: self.number_of_instructions]:
            updates = trigger.duration * self.rate.to_rate() / 1000.0
            self.request.insert_byte(address, self.encode_triggers(trigger))
            self.request.insert_uint16(
                address + 1,
                int(saturate(trigger.code, 0, UINT16_MAX)),
            )
            self.request.insert_uint16(
                address + 3,
                int(saturate(updates, 1, UINT16_MAX)),
            )
            address += self.TRIGGER_SIZE

    def __str__(self) -> str:
        return "[0x14] Set Trigger Sequence"
