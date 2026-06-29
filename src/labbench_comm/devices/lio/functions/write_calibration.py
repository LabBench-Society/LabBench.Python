from labbench_comm.devices.lio.definitions import CalibratorID
from labbench_comm.devices.lio.functions.base import (
    CALIBRATION_Q,
    _LIOFunction,
)


class WriteCalibration(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x41

    def __init__(self) -> None:
        super().__init__(request_length=13, response_length=0)

    @property
    def calibrator(self) -> CalibratorID:
        return CalibratorID(self.request.get_byte(0))

    @calibrator.setter
    def calibrator(self, value: CalibratorID) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def valid_marker(self) -> int:
        return self.request.get_byte(1)

    @valid_marker.setter
    def valid_marker(self, value: int) -> None:
        self.request.insert_byte(1, value)

    @property
    def a(self) -> float:
        return self.ab / float(2 ** CALIBRATION_Q)

    @property
    def ab(self) -> int:
        return self.request.get_int32(2)

    @ab.setter
    def ab(self, value: int) -> None:
        self.request.insert_int32(2, value)

    @property
    def b(self) -> float:
        return self.bb / float(2 ** CALIBRATION_Q)

    @property
    def bb(self) -> int:
        return self.request.get_int32(6)

    @bb.setter
    def bb(self, value: int) -> None:
        self.request.insert_int32(6, value)

    @property
    def maximum(self) -> int:
        return self.request.get_uint16(10)

    @maximum.setter
    def maximum(self, value: int) -> None:
        self.request.insert_uint16(10, value)

    @property
    def checksum(self) -> int:
        return self.request.get_byte(12)

    @checksum.setter
    def checksum(self, value: int) -> None:
        self.request.insert_byte(12, value)

    def __str__(self) -> str:
        return "[0x41] Write Calibration Record"
