from labbench_comm.devices.lio.definitions import ResponseDevice, ResponseSubClass
from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetRequiredDevices(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x21

    def __init__(self) -> None:
        super().__init__(request_length=4, response_length=0)
        self.port01 = ResponseDevice.DEVICE_NONE
        self.port01_subclass = ResponseSubClass.DEVICE_SUBCLASS_NONE
        self.port02 = ResponseDevice.DEVICE_NONE
        self.port02_subclass = ResponseSubClass.DEVICE_SUBCLASS_NONE

    @property
    def port01(self) -> ResponseDevice:
        return ResponseDevice(self.request.get_byte(0))

    @port01.setter
    def port01(self, value: ResponseDevice) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def port01_subclass(self) -> ResponseSubClass:
        return ResponseSubClass(self.request.get_byte(1))

    @port01_subclass.setter
    def port01_subclass(self, value: ResponseSubClass) -> None:
        self.request.insert_byte(1, int(value))

    @property
    def port02(self) -> ResponseDevice:
        return ResponseDevice(self.request.get_byte(2))

    @port02.setter
    def port02(self, value: ResponseDevice) -> None:
        self.request.insert_byte(2, int(value))

    @property
    def port02_subclass(self) -> ResponseSubClass:
        return ResponseSubClass(self.request.get_byte(3))

    @port02_subclass.setter
    def port02_subclass(self, value: ResponseSubClass) -> None:
        self.request.insert_byte(3, int(value))

    def __str__(self) -> str:
        return "[0x21] Set Required Devices"
