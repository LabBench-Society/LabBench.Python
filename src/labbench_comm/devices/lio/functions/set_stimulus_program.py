from labbench_comm.protocols.packet import ChecksumAlgorithmType, Packet

from labbench_comm.devices.lio.definitions import (
    UINT16_MAX,
    UINT32_MAX,
    Instruction,
    InstructionType,
    UpdateRate,
    saturate,
)
from labbench_comm.devices.lio.functions.base import MAX_VOLTAGE, _LIOFunction


class SetStimulusProgram(_LIOFunction):
    MAX_NO_OF_INSTRUCTIONS = 256
    INSTRUCTION_SIZE = 7

    @property
    def code(self) -> int:
        return 0x13

    def __init__(self, rate: UpdateRate = UpdateRate.CLK20000Hz) -> None:
        super().__init__(request_length=0, response_length=0)
        self.rate = rate
        self.instructions: list[Instruction] = []

    def nop(self, duration: float) -> None:
        self.instructions.append(Instruction(InstructionType.NOP, 0.0, duration))

    def set(self, value: float, duration: float) -> None:
        self.instructions.append(Instruction(InstructionType.SET, value, duration))

    def inc(self, value: float, duration: float) -> None:
        self.instructions.append(Instruction(InstructionType.INC, value, duration))

    def dec(self, value: float, duration: float) -> None:
        self.instructions.append(Instruction(InstructionType.DEC, value, duration))

    @property
    def number_of_instructions(self) -> int:
        return min(len(self.instructions), self.MAX_NO_OF_INSTRUCTIONS)

    def encode_operand(self, instruction: Instruction) -> int:
        argument = instruction.argument

        if instruction.instruction_type is InstructionType.SET:
            argument = saturate(argument, -MAX_VOLTAGE, MAX_VOLTAGE) / MAX_VOLTAGE
            argument = UINT32_MAX * (argument + 1.0) / 2.0
        elif instruction.instruction_type is InstructionType.INC:
            if argument < 0:
                argument = 0
            argument = (UINT32_MAX / 2.0) * (
                1000.0 * (argument / MAX_VOLTAGE) / self.rate.to_rate()
            )
        elif instruction.instruction_type is InstructionType.DEC:
            if argument > 0:
                argument = 0
            argument = -(UINT32_MAX / 2.0) * (
                1000.0 * (argument / MAX_VOLTAGE) / self.rate.to_rate()
            )
        elif instruction.instruction_type is InstructionType.NOP:
            argument = 0

        return int(saturate(argument, 0, UINT32_MAX))

    def decode_operand(self, instruction_type: InstructionType, operand: int) -> float:
        if instruction_type is InstructionType.SET:
            return ((operand * 2.0 / UINT32_MAX) - 1.0) * MAX_VOLTAGE
        if instruction_type is InstructionType.INC:
            return operand * 2.0 / UINT32_MAX * self.rate.to_rate() / 1000.0 * MAX_VOLTAGE
        if instruction_type is InstructionType.DEC:
            return -operand * 2.0 / UINT32_MAX * self.rate.to_rate() / 1000.0 * MAX_VOLTAGE
        return 0.0

    def on_send(self) -> None:
        self.set_request(Packet(
            self.code,
            self.INSTRUCTION_SIZE * self.number_of_instructions,
            ChecksumAlgorithmType.CRC8CCITT,
        ))

        address = 0
        for instruction in self.instructions[: self.number_of_instructions]:
            updates = instruction.duration * self.rate.to_rate() / 1000.0
            operand = self.encode_operand(instruction)
            cycle = int(saturate(updates, 0, UINT16_MAX))

            self.request.insert_byte(address, int(instruction.instruction_type))
            self.request.insert_uint32(address + 1, operand)
            self.request.insert_uint16(address + 5, cycle)
            address += self.INSTRUCTION_SIZE

    def on_slave_received(self) -> None:
        count = self.request.length // self.INSTRUCTION_SIZE
        self.instructions.clear()

        for n in range(count):
            offset = n * self.INSTRUCTION_SIZE
            instruction_type = InstructionType(self.request.get_byte(offset))
            operand = self.request.get_uint32(offset + 1)
            cycle = self.request.get_uint16(offset + 5)
            duration = self.rate.samples_to_milliseconds(cycle)
            argument = self.decode_operand(instruction_type, operand)
            self.instructions.append(Instruction(instruction_type, argument, duration))

    def __str__(self) -> str:
        return "[0x13] Set Stimulus Program"
