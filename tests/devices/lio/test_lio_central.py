import pytest

from labbench_comm.devices.lio import (
    AnalogChannel,
    AnalogInputMessage,
    ButtonMessage,
    ClearPrograms,
    DeviceState,
    EcpError,
    EventID,
    EventMessage,
    GetAnalogSignal,
    GetEvent,
    GetInterfaceStatus,
    InstructionType,
    LIOCentral,
    Logic,
    ReadCalibration,
    ResponseDevice,
    ResponsePort,
    ResponseSubClass,
    SetInterfaceLogic,
    SetStimulusProgram,
    SetTrigger,
    SetTriggerSequence,
    SetVoltage,
    SetWaveform,
    SignalMessage,
    StatusMessage,
    SystemError,
    TriggerInstruction,
    UpdateRate,
    VoltageLevel,
    from_fixed_point,
    saturate,
)
from labbench_comm.protocols.bus_central import BusCentral
from labbench_comm.protocols.exceptions import InvalidMessageError
from labbench_comm.protocols.functions.device_identification import DeviceIdentification
from labbench_comm.protocols.functions.ping import Ping
from labbench_comm.protocols.manufacturer import Manufacturer
from labbench_comm.protocols.packet import ChecksumAlgorithmType, Packet


class FakeConnection:
    def __init__(self) -> None:
        self.destuffer = None

    def attach_destuffer(self, destuffer) -> None:
        self.destuffer = destuffer

    @property
    def is_open(self) -> bool:
        return False

    async def open(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def write_bytes(self, data: bytes) -> None:
        pass


def make_device() -> LIOCentral:
    return LIOCentral(BusCentral(FakeConnection()))


def make_identification(
    manufacturer_id: Manufacturer,
    device_id: int,
    major_version: int = 2,
) -> DeviceIdentification:
    ident = DeviceIdentification()
    ident.manufacturer_id = manufacturer_id
    ident.device_id = device_id
    ident.major_version = major_version
    return ident


@pytest.mark.unittest
def test_lio_central_import_and_constructor_defaults():
    device = make_device()

    assert isinstance(device, LIOCentral)
    assert device.baudrate == 57600
    assert device.retries == 3
    assert str(device) == "LabBench I/O"


@pytest.mark.unittest
def test_lio_central_is_compatible_for_lio_identification():
    device = make_device()
    ident = make_identification(Manufacturer.InventorsWay, 2)

    assert device.is_compatible(ident)


@pytest.mark.unittest
def test_lio_central_rejects_wrong_manufacturer():
    device = make_device()
    ident = make_identification(Manufacturer.Detectronic, 2)

    assert not device.is_compatible(ident)


@pytest.mark.unittest
def test_lio_central_rejects_wrong_device_id():
    device = make_device()
    ident = make_identification(Manufacturer.InventorsWay, 4)

    assert not device.is_compatible(ident)


@pytest.mark.unittest
def test_lio_central_rejects_old_major_version():
    device = make_device()
    ident = make_identification(Manufacturer.InventorsWay, 2, major_version=1)

    assert not device.is_compatible(ident)


@pytest.mark.unittest
def test_lio_central_rejects_non_identification_function():
    device = make_device()

    assert not device.is_compatible(Ping())


@pytest.mark.unittest
def test_lio_central_unknown_peripheral_error_string():
    device = make_device()

    assert device.get_peripheral_error_string(17) == (
        EcpError.ECP_CANNOT_SET_VOLTAGE_AS_PROGRAM_IS_ACTIVE_ERR.name
    )
    assert device.get_peripheral_error_string(255) == "Unknown LIO error (255)"


@pytest.mark.unittest
def test_lio_helpers_and_enum_values():
    assert AnalogChannel.SUPPLY_VOLTAGE == 11
    assert ResponseDevice.DEVICE_REPONSE_INPUT == 7
    assert UpdateRate.CLK20000Hz.to_rate() == 20000
    assert UpdateRate.from_rate(1000) is UpdateRate.CLK1000Hz
    assert UpdateRate.CLK1000Hz.milliseconds_to_samples(2.5) == 2
    assert UpdateRate.CLK1000Hz.samples_to_milliseconds(2) == 2.0
    assert UpdateRate.CLK1000Hz.sampling_error_in_milliseconds(2.6) == pytest.approx(0.4)
    assert from_fixed_point(64, 5) == 2.0
    assert saturate(12, 0, 10) == 10


@pytest.mark.unittest
def test_lio_subpackage_imports_remain_available():
    from labbench_comm.devices.lio.functions import SetVoltage as FunctionSetVoltage
    from labbench_comm.devices.lio.messages import StatusMessage as MessageStatus

    assert FunctionSetVoltage is SetVoltage
    assert MessageStatus is StatusMessage


@pytest.mark.unittest
@pytest.mark.parametrize(
    "function,code,request_length,response_length",
    [
        (ClearPrograms(), 0x19, 0, 0),
        (GetAnalogSignal(), 0x25, 1, 2),
        (GetEvent(), 0x46, 1, 73),
        (GetInterfaceStatus(), 0x50, 0, 4),
        (ReadCalibration(), 0x42, 1, 12),
    ],
)
def test_lio_static_function_packet_shapes(function, code, request_length, response_length):
    assert function.code == code
    assert function.request.length == request_length
    assert function.response.length == response_length
    assert function.create_dispatcher().code == code


@pytest.mark.unittest
def test_get_analog_signal_properties():
    function = GetAnalogSignal()
    function.channel = AnalogChannel.TRIG_VTH
    function.value = 1234

    assert function.request.get_byte(0) == AnalogChannel.TRIG_VTH
    assert function.channel is AnalogChannel.TRIG_VTH
    assert function.response.get_uint16(0) == 1234
    assert function.value == 1234


@pytest.mark.unittest
def test_read_calibration_decodes_fixed_point_record():
    function = ReadCalibration()
    function.response.insert_byte(0, 0xC9)
    function.response.insert_int32(1, 8192)
    function.response.insert_int32(5, -4096)
    function.response.insert_uint16(9, 1000)
    function.response.insert_byte(11, 0x55)

    assert function.valid_marker
    assert function.a == 2.0
    assert function.ab == 8192
    assert function.b == -1.0
    assert function.bb == -4096
    assert function.maximum == 1000
    assert function.checksum == 0x55


@pytest.mark.unittest
def test_set_interface_logic_rejects_invalid_voltage_level():
    function = SetInterfaceLogic()
    function.low_byte_level = VoltageLevel.V3p3
    function.high_byte_level = VoltageLevel.V5p0
    function.logic = Logic.Negative

    assert function.request.get_byte(0) == VoltageLevel.V3p3
    assert function.request.get_byte(1) == VoltageLevel.V5p0
    assert function.request.get_byte(2) == Logic.Negative

    with pytest.raises(ValueError):
        function.low_byte_level = VoltageLevel.Invalid


@pytest.mark.unittest
def test_set_trigger_bitfield_and_code():
    function = SetTrigger()
    function.trigger = True
    function.stimulus_trigger = True
    function.trigger_code = 0x1234

    assert function.request.get_byte(0) == 0x03
    assert function.trigger
    assert function.stimulus_trigger
    assert function.trigger_code == 0x1234

    function.trigger = False
    assert function.request.get_byte(0) == 0x02


@pytest.mark.unittest
def test_set_stimulus_program_serializes_and_decodes_dynamic_packet():
    function = SetStimulusProgram(UpdateRate.CLK1000Hz)
    function.set(5.0, 10.0)
    function.inc(1.0, 5.0)
    function.dec(-1.0, 5.0)
    function.nop(1.0)

    function.on_send()

    assert function.request.length == 28
    assert function.request.checksum_algorithm is ChecksumAlgorithmType.CRC8CCITT
    assert function.request.get_byte(0) == InstructionType.SET
    assert function.request.get_uint16(5) == 10

    decoded = SetStimulusProgram(UpdateRate.CLK1000Hz)
    decoded.set_request(function.request)
    decoded.on_slave_received()

    assert len(decoded.instructions) == 4
    assert decoded.instructions[0].instruction_type is InstructionType.SET
    assert decoded.instructions[0].argument == pytest.approx(5.0)
    assert decoded.instructions[1].instruction_type is InstructionType.INC
    assert decoded.instructions[1].argument == pytest.approx(1.0, rel=1e-6)
    assert decoded.instructions[2].instruction_type is InstructionType.DEC
    assert decoded.instructions[2].argument == pytest.approx(-1.0, rel=1e-6)


@pytest.mark.unittest
def test_set_trigger_sequence_serializes_dynamic_packet():
    function = SetTriggerSequence()
    function.rate = UpdateRate.CLK1000Hz
    function.add(TriggerInstruction(300000, True, False), duration=2.0)
    function.add(TriggerInstruction(7, False, True), duration=0.1)

    function.on_send()

    assert function.request.length == 10
    assert function.request.checksum_algorithm is ChecksumAlgorithmType.CRC8CCITT
    assert function.request.get_byte(0) == 0x01
    assert function.request.get_uint16(1) == 0xFFFF
    assert function.request.get_uint16(3) == 2
    assert function.request.get_byte(5) == 0x02
    assert function.request.get_uint16(8) == 1


@pytest.mark.unittest
def test_set_voltage_and_waveform_dynamic_packets():
    voltage = SetVoltage()
    voltage.voltage = 20.0
    voltage.on_send()

    assert voltage.voltage == 10.0
    assert voltage.request.get_uint32(0) == 0xFFFFFFFF

    waveform = SetWaveform()
    waveform.rate = UpdateRate.CLK1000Hz
    waveform.repeat = 2
    waveform.offset = 1.0
    waveform.period = 10.0
    waveform.samples.extend([-2.0, 0.0, 0.5, 2.0])
    waveform.on_send()

    assert waveform.request.length == 14
    assert waveform.request.checksum_algorithm is ChecksumAlgorithmType.CRC8CCITT
    assert waveform.request.get_uint16(0) == 2
    assert waveform.request.get_uint16(2) == 1
    assert waveform.request.get_uint16(4) == 10
    assert waveform.request.get_int16(6) == -4095
    assert waveform.request.get_int16(10) == 2047
    assert waveform.request.get_int16(12) == 4095


@pytest.mark.unittest
def test_lio_messages_decode_and_validate_lengths():
    status_packet = Packet(0x80, 7)
    status_packet.insert_byte(0, 0)
    status_packet.insert_byte(1, ResponseDevice.DEVICE_BUTTON)
    status_packet.insert_byte(2, ResponseSubClass.DEVICE_SUBCLASS02)
    status_packet.insert_byte(3, ResponseDevice.DEVICE_NONE)
    status_packet.insert_byte(4, ResponseSubClass.DEVICE_SUBCLASS_NONE)
    status_packet.insert_byte(5, 1)
    status_packet.insert_byte(6, SystemError.NO_POWER_ERROR)
    status = StatusMessage(status_packet)

    assert status.state is DeviceState.STATE_IDLE
    assert status.port01 is ResponseDevice.DEVICE_BUTTON
    assert status.port01_subclass is ResponseSubClass.DEVICE_SUBCLASS02
    assert status.power
    assert status.error is SystemError.NO_POWER_ERROR

    bad_packet = Packet(0x80, 6)
    with pytest.raises(InvalidMessageError):
        StatusMessage(bad_packet)


@pytest.mark.unittest
def test_signal_message_decodes_scaling():
    packet = Packet(0x90, 21)
    packet.insert_byte(0, ResponsePort.RESPONSE_PORT01)
    packet.insert_byte(1, ResponseDevice.DEVICE_RESPONSE)
    packet.insert_byte(2, ResponseSubClass.DEVICE_SUBCLASS01)
    packet.insert_uint16(3, 512)
    packet.insert_int32(5, 4096)
    packet.insert_int32(9, 2048)
    packet.insert_uint16(13, 1024)
    packet.insert_int16(15, 64)
    packet.insert_int16(17, 96)
    packet.insert_int16(19, -32)

    message = SignalMessage(packet)

    assert message.value == 0.5
    assert message.a == 1.0
    assert message.b == 0.5
    assert message.target == 2.0
    assert message.high_limit == 3.0
    assert message.low_limit == -1.0
    assert message.voltage == pytest.approx(1.0004887585)


@pytest.mark.unittest
def test_lio_central_updates_state_and_callbacks_from_messages():
    device = make_device()
    status_seen = []
    signal_seen = []
    event_seen = []
    device.status_received.append(lambda sender, msg: status_seen.append((sender, msg)))
    device.signal_received.append(lambda sender, msg: signal_seen.append((sender, msg)))
    device.event_received.append(lambda sender, msg: event_seen.append((sender, msg)))

    status_packet = Packet(0x80, 7)
    status_packet.insert_byte(0, 0)
    status_packet.insert_byte(1, ResponseDevice.DEVICE_RESPONSE)
    status_packet.insert_byte(2, ResponseSubClass.DEVICE_SUBCLASS01)
    status_packet.insert_byte(3, ResponseDevice.DEVICE_NONE)
    status_packet.insert_byte(4, ResponseSubClass.DEVICE_SUBCLASS_NONE)
    status_packet.insert_byte(5, 1)
    status_packet.insert_byte(6, SystemError.NO_ERROR)

    device.on_status_message(StatusMessage(status_packet))

    assert device.state is DeviceState.STATE_IDLE
    assert device.port01 is ResponseDevice.DEVICE_RESPONSE
    assert device.power
    assert status_seen[0][0] is device

    signal_packet = Packet(0x90, 21)
    signal_packet.insert_byte(0, ResponsePort.RESPONSE_PORT01)
    signal_packet.insert_byte(1, ResponseDevice.DEVICE_RESPONSE)
    signal_packet.insert_byte(2, ResponseSubClass.DEVICE_SUBCLASS01)
    signal_packet.insert_uint16(3, 512)
    signal_packet.insert_int32(5, 4096)
    signal_packet.insert_int32(9, 0)
    signal_packet.insert_uint16(13, 1024)
    signal_packet.insert_int16(15, 64)
    signal_packet.insert_int16(17, 96)
    signal_packet.insert_int16(19, 32)

    device.on_signal_message(SignalMessage(signal_packet))

    assert device.value01 == 0.5
    assert device.target01 == 2.0
    assert signal_seen[0][0] is device

    event = EventMessage()
    event.event = EventID.EVT_PROGRAM_COMPLETE
    device.on_event_message(event)

    assert event_seen[0][1].event is EventID.EVT_PROGRAM_COMPLETE


@pytest.mark.unittest
def test_other_lio_messages_decode_time_and_values():
    button_packet = Packet(0x91, 10)
    button_packet.insert_byte(0, ResponsePort.RESPONSE_PORT02)
    button_packet.insert_byte(1, ResponseDevice.DEVICE_BUTTON)
    button_packet.insert_byte(2, ResponseSubClass.DEVICE_SUBCLASS01)
    button_packet.insert_byte(3, 4)
    button_packet.insert_bool(4, True)
    button_packet.insert_byte(5, 2)
    button_packet.insert_uint32(6, 100)

    button = ButtonMessage(button_packet)
    assert button.port is ResponsePort.RESPONSE_PORT02
    assert button.button == 4
    assert button.state
    assert button.time == 50

    analog_packet = Packet(0x94, 13)
    analog_packet.insert_byte(0, 3)
    analog_packet.insert_uint16(1, 256)
    analog_packet.insert_int32(3, 4096)
    analog_packet.insert_int32(7, 0)
    analog_packet.insert_uint16(11, 512)
    analog = AnalogInputMessage(analog_packet)

    assert analog.pin == 3
    assert analog.value == 0.5
    assert analog.voltage == pytest.approx(256 / 1023)
