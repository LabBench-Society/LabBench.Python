from labbench_comm.devices.lio.definitions import CalibratorID
from labbench_comm.devices.lio.functions.base import (
    CALIBRATION_Q,
    CALIBRATION_RECORD_SIZE,
    CALIBRATION_VALID_MARKER,
    _LIOFunction,
)


class ReadCalibration(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x42

    def __init__(self) -> None:
        super().__init__(request_length=1, response_length=CALIBRATION_RECORD_SIZE)
        self.calibrator = CalibratorID.ID_RSP01_CALIBRATOR

    @property
    def calibrator(self) -> CalibratorID:
        return CalibratorID(self.request.get_byte(0))

    @calibrator.setter
    def calibrator(self, value: CalibratorID) -> None:
        self.request.insert_byte(0, int(value))

    @property
    def valid_marker(self) -> bool:
        return self.response.get_byte(0) == CALIBRATION_VALID_MARKER

    @property
    def a(self) -> float:
        return self.ab / float(2 ** CALIBRATION_Q)

    @property
    def ab(self) -> int:
        return self.response.get_int32(1)

    @property
    def b(self) -> float:
        return self.bb / float(2 ** CALIBRATION_Q)

    @property
    def bb(self) -> int:
        return self.response.get_int32(5)

    @property
    def maximum(self) -> int:
        return self.response.get_uint16(9)

    @property
    def checksum(self) -> int:
        return self.response.get_byte(CALIBRATION_RECORD_SIZE - 1)

    def __str__(self) -> str:
        return "[0x42] Read Calibration Record"
