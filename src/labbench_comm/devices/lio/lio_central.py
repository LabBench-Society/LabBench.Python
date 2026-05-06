from labbench_comm.protocols.device import Device
from labbench_comm.protocols.device_function import DeviceFunction
from labbench_comm.protocols.functions.device_identification import DeviceIdentification
from labbench_comm.protocols.manufacturer import Manufacturer


class LIOCentral(Device):
    def __init__(self, bus) -> None:
        super().__init__(bus)

        self.baudrate = 57600
        self.retries = 3

    def get_peripheral_error_string(self, error_code: int) -> str:
        return f"Unknown LIO error ({error_code})"

    def is_compatible(self, function: DeviceFunction) -> bool:
        if not isinstance(function, DeviceIdentification):
            return False

        return (
            function.manufacturer_id == Manufacturer.InventorsWay
            and function.device_id == 2
        )

    def __str__(self) -> str:
        return "LIO Device"
