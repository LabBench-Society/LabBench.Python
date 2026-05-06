from labbench_comm.devices.lio.functions.set_signal_sample_period import (
    SetSignalSamplePeriod,
)


class SetTriggerArmingPeriod(SetSignalSamplePeriod):
    @property
    def code(self) -> int:
        return 0x23

    def __str__(self) -> str:
        return "[0x23] Set Trigger Arming Period"
