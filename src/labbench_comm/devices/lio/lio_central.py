from labbench_comm.protocols.device import Device
from labbench_comm.protocols.device_function import DeviceFunction
from labbench_comm.protocols.functions.device_identification import DeviceIdentification
from labbench_comm.protocols.manufacturer import Manufacturer

from labbench_comm.devices.lio.definitions import (
    DeviceState,
    EcpError,
    ResponseDevice,
    ResponsePort,
    ResponseSubClass,
    SystemError,
)
from labbench_comm.devices.lio.messages import (
    AnalogInputMessage,
    ButtonMessage,
    EventMessage,
    SignalMessage,
    StatusMessage,
    ThresholdMessage,
    TriggerMessage,
)


class LIOCentral(Device):
    def __init__(self, bus) -> None:
        super().__init__(bus)

        self.baudrate = 57600
        self.retries = 3

        self.add_message(EventMessage())
        self.add_message(StatusMessage())
        self.add_message(SignalMessage())
        self.add_message(ButtonMessage())
        self.add_message(TriggerMessage())
        self.add_message(AnalogInputMessage())
        self.add_message(ThresholdMessage())

        self.port01 = ResponseDevice.DEVICE_NONE
        self.port01_subclass = ResponseSubClass.DEVICE_SUBCLASS_NONE
        self.value01 = 0.0
        self.signal01 = 0.0
        self.range01 = 0.0
        self.a01 = 0.0
        self.b01 = 0.0
        self.voltage01 = 0.0
        self.target01 = 0.0
        self.target01_low_limit = 0.0
        self.target01_high_limit = 0.0

        self.port02 = ResponseDevice.DEVICE_NONE
        self.port02_subclass = ResponseSubClass.DEVICE_SUBCLASS_NONE
        self.value02 = 0.0
        self.signal02 = 0.0
        self.range02 = 0.0
        self.a02 = 0.0
        self.b02 = 0.0
        self.voltage02 = 0.0
        self.target02 = 0.0
        self.target02_low_limit = 0.0
        self.target02_high_limit = 0.0

        self.state = DeviceState.STATE_NOT_CONNECTED
        self.error = SystemError.NO_ERROR
        self.power = False
        self.log_events = True

        self.status_received = []
        self.event_received = []
        self.signal_received = []
        self.button_received = []
        self.analog_input_received = []
        self.trigger_received = []
        self.threshold_received = []

    def get_peripheral_error_string(self, error_code: int) -> str:
        try:
            return EcpError(error_code).name
        except ValueError:
            return f"Unknown LIO error ({error_code})"

    def on_status_message(self, message: StatusMessage) -> None:
        if message is None:
            return

        self.state = message.state
        self.port01 = message.port01
        self.port01_subclass = message.port01_subclass
        self.port02 = message.port02
        self.port02_subclass = message.port02_subclass
        self.power = message.power
        self.error = message.error

        if self.port01 == ResponseDevice.DEVICE_NONE:
            self.value01 = 0.0
            self.signal01 = 0.0
            self.range01 = 0.0

        if self.port02 == ResponseDevice.DEVICE_NONE:
            self.value02 = 0.0
            self.signal02 = 0.0
            self.range02 = 0.0

        for cb in self.status_received:
            cb(self, message)

    def on_event_message(self, message: EventMessage) -> None:
        if message is None:
            return

        for cb in self.event_received:
            cb(self, message)

    def on_signal_message(self, message: SignalMessage) -> None:
        if message is None:
            return

        if message.port == ResponsePort.RESPONSE_PORT01:
            self.value01 = message.value
            self.signal01 = message.signal
            self.range01 = message.range
            self.a01 = message.a
            self.b01 = message.b
            self.voltage01 = message.voltage
            self.target01 = message.target
            self.target01_high_limit = message.high_limit
            self.target01_low_limit = message.low_limit

        if message.port == ResponsePort.RESPONSE_PORT02:
            self.value02 = message.value
            self.signal02 = message.signal
            self.range02 = message.range
            self.a02 = message.a
            self.b02 = message.b
            self.voltage02 = message.voltage
            self.target02 = message.target
            self.target02_high_limit = message.high_limit
            self.target02_low_limit = message.low_limit

        for cb in self.signal_received:
            cb(self, message)

    def on_button_message(self, message: ButtonMessage) -> None:
        if message is None:
            return

        for cb in self.button_received:
            cb(self, message)

    def on_analog_input_message(self, message: AnalogInputMessage) -> None:
        if message is None:
            return

        for cb in self.analog_input_received:
            cb(self, message)

    def on_trigger_message(self, message: TriggerMessage) -> None:
        if message is None:
            return

        for cb in self.trigger_received:
            cb(self, message)

    def on_threshold_message(self, message: ThresholdMessage) -> None:
        if message is None:
            return

        for cb in self.threshold_received:
            cb(self, message)

    def is_compatible(self, function: DeviceFunction) -> bool:
        if not isinstance(function, DeviceIdentification):
            return False

        return (
            function.manufacturer_id == Manufacturer.InventorsWay
            and function.device_id == 2
            and function.major_version >= 2
        )

    def __str__(self) -> str:
        return "LabBench I/O"
