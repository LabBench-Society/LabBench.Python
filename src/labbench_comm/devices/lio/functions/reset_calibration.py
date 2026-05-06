from labbench_comm.devices.lio.functions.base import _LIOFunction


class ResetCalibration(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x43

    def __init__(self) -> None:
        super().__init__(request_length=0, response_length=0)

    def __str__(self) -> str:
        return "[0x43] Reset Calibration"
