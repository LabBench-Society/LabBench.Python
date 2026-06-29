from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


UINT16_MAX = 0xFFFF
UINT32_MAX = 0xFFFFFFFF


def saturate(value, lower, upper):
    if value < lower:
        return lower
    if value > upper:
        return upper
    return value


def from_fixed_point(value: int, q: int) -> float:
    return value / float(2 ** q)


class AnalogChannel(IntEnum):
    RES1_RATING = 0
    RES2_RATING = 1
    RES1_DETECT = 2
    RES2_DETECT = 3
    RES1_DDF06 = 4
    RES2_DDF06 = 5
    TRIG_S13 = 6
    TRIG_S25 = 7
    TRIG_MISC = 8
    TRIG_VTL = 9
    TRIG_VTH = 10
    SUPPLY_VOLTAGE = 11


class DeviceEventType(IntEnum):
    BUILD_EVENT = 0
    CALIBRATION_EVENT = 1


class EventID(IntEnum):
    EVT_NO_EVENT = 0
    EVT_BUTTON_PRESSED = 1
    EVT_12V_POWER_ON = 2
    EVT_12V_POWER_OFF = 3
    EVT_TRIG_IN_ACTIVE = 4
    EVT_PROGRAM_COMPLETE = 5
    EVT_PROGRAM_TIMEOUT = 6
    EVT_TRIGGER_TIMEOUT = 7
    EVT_TRIGGER_PORT01 = 8
    EVT_TRIGGER_PORT02 = 9
    EVT_THRESHOLD_PORT01 = 10
    EVT_THRESHOLD_PORT02 = 11


class CalibratorID(IntEnum):
    ID_RSP01_CALIBRATOR = 0
    ID_RSP02_CALIBRATOR = 1


class DeviceState(IntEnum):
    STATE_IDLE = 0
    STATE_PENDING = 1
    STATE_ACTIVE = 2
    STATE_ERROR = 3


class EcpError(IntEnum):
    ECP_NO_ERROR = 0
    ECP_UNKNOWN_FUNCTION_ERR = 1
    ECP_CHECKSUM_ERR = 2
    ECP_INVALID_REQUEST_LENGTH_ERR = 3
    ECP_INVALID_NUMBER_OF_DEBUG_SIGNALS_ERR = 4
    ECP_ATTEMPT_TO_SET_PROGRAM_WHILE_SYSTEM_IS_NOT_IDLE_ERR = 5
    ECP_INVALID_LENGTH_OF_STIMULUS_PROGRAM_ERR = 6
    ECP_STIMULUS_PROGRAM_IS_TOO_LONG_ERR = 7
    ECP_ATTEMPT_TO_SET_TRIGGER_SEQUENCE_WHILE_SYSTEM_IS_NOT_IDLE_ERR = 8
    ECP_ATTEMPT_TO_SET_WAVEFORM_WHILE_SYSTEM_IS_NOT_IDLE_ERR = 9
    ECP_WAVEFORM_TOO_SHORT_ERR = 10
    ECP_WAVEFORM_WRONG_SIZE_ERR = 11
    ECP_WAVEFORM_TOO_LONG_ERR = 12
    ECP_WAVEFORM_REPEATED_ZERO_TIMES_ERR = 13
    ECP_STARTING_GENERATOR_WHILE_NOT_IDLE_ERR = 14
    ECP_GENERATOR_NOT_STARTED_ERR = 15
    ECP_INVALID_TRIGGER_ERR = 16
    ECP_CANNOT_SET_VOLTAGE_AS_PROGRAM_IS_ACTIVE_ERR = 17
    ECP_NO_SUITABLE_RESPONSE_DEVICE_CONNECTED_ERR = 18
    ECP_TRIGGER_SYSTEM_NOT_MANUAL_MODE_ERR = 19
    ECP_INVALID_LENGTH_OF_TRIGGER_SEQUENCE_ERR = 20
    ECP_TRIGGER_SEQUENCE_TOO_LONG_ERR = 21
    ECP_INVALID_UPDATE_RATE_ERR = 22
    ECP_INVALID_EVENT_ADDRESS_ERR = 23
    ECP_INVALID_STIMULUS_PROGRAM_TYPE_ERR = 24
    ECP_STIMULUS_PERIOD_TOO_SHORT_ERR = 25
    ECP_CANNOT_SET_BUILD_EVENT_ERR = 26
    ECP_COULD_NOT_SAVE_TO_EEPROM_ERR = 27
    ECP_INVALID_CALIBRATION_ADDRESS_ERR = 28
    ECP_CANNOT_RESTART_AN_INTERNALLY_TRIGGERED_PROGRAM_ERR = 29
    ECP_INVALID_PORT_ERR = 30
    ECP_I2C_WRITE_FAILED_ERR = 31
    ECP_I2C_READ_FAILED_ERR = 32
    ECP_DATA_VERIFY_FAILED_ERR = 33
    ECP_SAMPLE_PERIOD_TOO_LOW_ERR = 34
    ECP_SAMPLE_PERIOD_TOO_HIGH_ERR = 35
    ECP_INVALID_PARAMTER_ERR = 36
    ECP_INVALID_STATE_ERR = 37
    ECP_NO_PROGRAM_ERR = 38


class InputTriggerSource(IntEnum):
    TRIG_NONE = 0
    TRIG_IN = 1
    TRIG_BUTTON = 2
    TRIG_TRIGGER_PORT01 = 3
    TRIG_TRIGGER_PORT02 = 4


class InstructionType(IntEnum):
    NOP = 0x00
    INC = 0x02
    DEC = 0x04
    SET = 0x06


class Logic(IntEnum):
    Positive = 0
    Negative = 1


class ProgramType(IntEnum):
    PRG_NONE = 0
    PRG_PROGRAM = 1
    PRG_WAVEFORM = 2


class ResponseDevice(IntEnum):
    DEVICE_NONE = 0
    DEVICE_SCALE = 1
    DEVICE_DIGITAL = 2
    DEVICE_BUTTON = 3
    DEVICE_RESERVED01 = 4
    DEVICE_SENSOR = 5
    DEVICE_TRIGGER = 6
    DEVICE_RESPONSE_INPUT = 7
    DEVICE_RESERVED02 = 8
    DEVICE_RESERVED03 = 9
    DEVICE_RESPONSE = 4
    DEVICE_REPONSE_INPUT = 7


class ResponsePort(IntEnum):
    RESPONSE_PORT01 = 0
    RESPONSE_PORT02 = 1


class ResponseSubClass(IntEnum):
    DEVICE_SUBCLASS_NONE = 0
    DEVICE_SUBCLASS01 = 1
    DEVICE_SUBCLASS02 = 2
    DEVICE_SUBCLASS03 = 3
    DEVICE_SUBCLASS04 = 4
    DEVICE_SUBCLASS05 = 5
    DEVICE_SUBCLASS06 = 6
    DEVICE_SUBCLASS07 = 7
    DEVICE_SUBCLASS08 = 8
    DEVICE_SUBCLASS09 = 9


class StimulusFeedbackTrigger(IntEnum):
    Timed = 0
    Button = 1
    Trigger = 2


class SystemError(IntEnum):
    NO_ERROR = 0
    NO_POWER_ERROR = 1
    INCORRECT_RESPONSE_DEVICE = 2
    INCORRECT_INTERFACE_VOLTAGE_LEVELS = 3


class TimingSource(IntEnum):
    SOURCE_TRIG_IN = 0
    SOURCE_GENERATOR_START = 1
    SOURCE_PORT01 = 2
    SOURCE_PORT02 = 3
    SOURCE_EOL = 4


class VoltageLevel(IntEnum):
    Unconnected = 0
    V3p3 = 1
    V5p0 = 2
    Invalid = 3


class UpdateRate(IntEnum):
    CLK125Hz = 0
    CLK250Hz = 1
    CLK500Hz = 2
    CLK1000Hz = 3
    CLK2000Hz = 4
    CLK5000Hz = 5
    CLK10000Hz = 6
    CLK20000Hz = 7

    def to_rate(self) -> float:
        return {
            UpdateRate.CLK125Hz: 125.0,
            UpdateRate.CLK250Hz: 250.0,
            UpdateRate.CLK500Hz: 500.0,
            UpdateRate.CLK1000Hz: 1000.0,
            UpdateRate.CLK2000Hz: 2000.0,
            UpdateRate.CLK5000Hz: 5000.0,
            UpdateRate.CLK10000Hz: 10000.0,
            UpdateRate.CLK20000Hz: 20000.0,
        }[self]

    @classmethod
    def from_rate(cls, rate: int) -> "UpdateRate":
        for candidate in cls:
            if candidate.to_rate() == rate:
                return candidate
        raise ValueError(f"Unsupported update rate {rate}Hz")

    def milliseconds_to_samples(self, time_ms: float) -> int:
        return round(self.to_rate() * time_ms / 1000.0)

    def seconds_to_samples(self, time_s: float) -> int:
        return round(self.to_rate() * time_s)

    def samples_to_milliseconds(self, samples: int) -> float:
        return 1000.0 * samples / self.to_rate()

    def samples_to_seconds(self, samples: int) -> float:
        return samples / self.to_rate()

    def sampling_error_in_milliseconds(self, time_ms: float) -> float:
        samples = self.milliseconds_to_samples(time_ms)
        return abs(time_ms - self.samples_to_milliseconds(samples))


def get_system_error_description(error: SystemError) -> str:
    if error is SystemError.NO_ERROR:
        return ""
    if error is SystemError.NO_POWER_ERROR:
        return (
            "The device is not connected to 24V power. "
            "Please check that Power Supply is connected."
        )
    if error is SystemError.INCORRECT_RESPONSE_DEVICE:
        return "Incorrect response device has been connected to a Response Port"
    if error is SystemError.INCORRECT_INTERFACE_VOLTAGE_LEVELS:
        return (
            "An incorrect trigger cable has been connected to the "
            "TRIGGER INTERFACE port."
        )
    return ""


@dataclass
class Instruction:
    instruction_type: InstructionType = InstructionType.NOP
    argument: float = 0.0
    duration: float = 0.0

    def __str__(self) -> str:
        if self.instruction_type is InstructionType.SET:
            return f"{self.instruction_type.name} ({self.argument}V:{self.duration}ms)"
        if self.instruction_type is InstructionType.INC:
            return f"{self.instruction_type.name} ({self.argument}V/ms:{self.duration}ms)"
        if self.instruction_type is InstructionType.DEC:
            return f"{self.instruction_type.name} (-{self.argument}V/ms:{self.duration}ms)"
        if self.instruction_type is InstructionType.NOP:
            return f"{self.instruction_type.name} ({self.duration})"
        return "UNKNOWN INSTRUCTION"


@dataclass
class TriggerInstruction:
    code: int = 0
    trigger_out: bool = False
    stimulus_trigger_out: bool = False
    duration: float = 1.0

    def __post_init__(self) -> None:
        self.code = int(saturate(self.code, 0, UINT16_MAX))

    def __str__(self) -> str:
        return (
            f"TRIG: {self.trigger_out}:{self.stimulus_trigger_out}:"
            f"{self.code} for {self.duration}ms"
        )
