import math
import pytest

from labbench_comm.devices.cpar.waveform import WaveformInstruction
from labbench_comm.devices.cpar.instruction_codec import InstructionCodec
from labbench_comm.devices.cpar.definitions import WaveformInstructionType


# ---------------------------------------------------------------------------
# WaveformInstruction construction tests
# ---------------------------------------------------------------------------

@pytest.mark.unittest
def test_default_instruction():
    instr = WaveformInstruction()

    assert instr.operand is WaveformInstructionType.TRIG
    assert instr.argument == 0.0
    assert instr.time == 1.0


@pytest.mark.unittest
def test_increment_factory():
    instr = WaveformInstruction.increment(delta=2.5, time=1.2)

    assert instr.operand is WaveformInstructionType.INC
    assert instr.argument == 2.5
    assert instr.time == 1.2


@pytest.mark.unittest
def test_decrement_factory():
    instr = WaveformInstruction.decrement(delta=1.0, time=0.5)

    assert instr.operand is WaveformInstructionType.DEC
    assert instr.argument == 1.0
    assert instr.time == 0.5


@pytest.mark.unittest
def test_step_factory():
    instr = WaveformInstruction.step(pressure=30.0, time=3.0)

    assert instr.operand is WaveformInstructionType.STEP
    assert instr.argument == 30.0
    assert instr.time == 3.0


@pytest.mark.unittest
def test_zero_factory():
    instr = WaveformInstruction.zero()

    assert instr.operand is WaveformInstructionType.STEP
    assert instr.argument == 0.0
    assert instr.time == 0.0


# ---------------------------------------------------------------------------
# String formatting tests
# ---------------------------------------------------------------------------

@pytest.mark.unittest
def test_str_formats():
    assert "INC" in str(WaveformInstruction.increment(1.0, 2.0))
    assert "DEC" in str(WaveformInstruction.decrement(1.0, 2.0))
    assert "STEP" in str(WaveformInstruction.step(10.0, 1.0))
    assert "TRIG" in str(WaveformInstruction())


# ---------------------------------------------------------------------------
# InstructionCodec encoding length
# ---------------------------------------------------------------------------

@pytest.mark.unittest
def test_encode_length():
    instr = WaveformInstruction.step(20.0, 1.0)
    encoded = InstructionCodec.encode(instr)

    assert isinstance(encoded, bytes)
    assert len(encoded) == InstructionCodec.INSTRUCTIONS_LENGTH


# ---------------------------------------------------------------------------
# Encode / Decode round-trip tests
# ---------------------------------------------------------------------------

@pytest.mark.unittest
@pytest.mark.parametrize(
    "instruction",
    [
        WaveformInstruction.step(25.0, 5.0),
        WaveformInstruction.increment(2.0, 1.0),
        WaveformInstruction.decrement(1.5, 2.5),
        WaveformInstruction(),
        WaveformInstruction.zero(),
    ],
)
def test_encode_decode_roundtrip(instruction):
    encoded = InstructionCodec.encode(instruction)
    decoded = InstructionCodec.decode(encoded)

    assert decoded.operand is instruction.operand
    assert math.isclose(decoded.argument, instruction.argument, rel_tol=1e-3)
    assert math.isclose(decoded.time, instruction.time, rel_tol=1e-3)


# ---------------------------------------------------------------------------
# Boundary and saturation tests
# ---------------------------------------------------------------------------

@pytest.mark.unittest
def test_pressure_clamping():
    instr = WaveformInstruction.step(
        pressure=InstructionCodec.MAX_PRESSURE * 2,
        time=1.0,
    )

    with pytest.raises(ValueError):
        InstructionCodec.encode(instr)


@pytest.mark.unittest
def test_negative_pressure_clamped_to_zero():
    instr = WaveformInstruction.step(-10.0, 1.0)

    encoded = InstructionCodec.encode(instr)
    decoded = InstructionCodec.decode(encoded)

    assert decoded.argument == 0.0


@pytest.mark.unittest
def test_time_upper_bound():
    instr = WaveformInstruction.step(
        pressure=10.0,
        time=InstructionCodec.MAX_TIME,
    )

    encoded = InstructionCodec.encode(instr)
    decoded = InstructionCodec.decode(encoded)

    assert math.isclose(decoded.time, InstructionCodec.MAX_TIME)


@pytest.mark.unittest
def test_time_exceeds_max_raises():
    instr = WaveformInstruction.step(
        pressure=10.0,
        time=InstructionCodec.MAX_TIME + 1.0,
    )

    with pytest.raises(ValueError):
        InstructionCodec.encode(instr)


# ---------------------------------------------------------------------------
# Decode validation tests
# ---------------------------------------------------------------------------

@pytest.mark.unittest
def test_decode_invalid_length():
    with pytest.raises(ValueError):
        InstructionCodec.decode(b"\x00\x01")


@pytest.mark.unittest
def test_decode_none():
    with pytest.raises(ValueError):
        InstructionCodec.decode(None)  # type: ignore


# ---------------------------------------------------------------------------
# Opcode correctness test
# ---------------------------------------------------------------------------

@pytest.mark.unittest
def test_opcode_bits_preserved():
    instr = WaveformInstruction.step(10.0, 1.0)
    encoded = InstructionCodec.encode(instr)

    padded = encoded + b"\x00" * (8 - len(encoded))
    binary = int.from_bytes(padded, byteorder="little")

    opcode = (binary >> 46) & 0x03
    assert opcode == instr.operand
