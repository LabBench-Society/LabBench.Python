from labbench_comm.protocols.packet import ChecksumAlgorithmType, Packet

from labbench_comm.devices.lio.definitions import UINT16_MAX, UpdateRate, saturate
from labbench_comm.devices.lio.functions.base import _LIOFunction


class SetWaveform(_LIOFunction):
    MAX_VALUE = 4095
    MAXIMUM_SAMPLE_COUNT = 1000

    @property
    def code(self) -> int:
        return 0x15

    def __init__(self) -> None:
        super().__init__(request_length=0, response_length=0)
        self.rate = UpdateRate.CLK20000Hz
        self.samples: list[float] = []
        self.repeat = 1
        self.period = 0.0
        self.offset = 0.0

    @property
    def waveform_length(self) -> float:
        return self.rate.samples_to_milliseconds(len(self.samples))

    @property
    def period_in_samples(self) -> int:
        return self.rate.milliseconds_to_samples(self.period)

    @property
    def offset_in_samples(self) -> int:
        return self.rate.milliseconds_to_samples(self.offset)

    def on_send(self) -> None:
        sample_count = len(self.samples)
        offset = self.offset_in_samples
        period = self.period_in_samples

        if sample_count > self.MAXIMUM_SAMPLE_COUNT:
            raise ValueError(
                f"Waveform cannot exceed the firmware limit of "
                f"{self.MAXIMUM_SAMPLE_COUNT} samples"
            )
        if period > UINT16_MAX:
            raise ValueError("Period cannot exceed UInt16 samples")
        if offset > UINT16_MAX:
            raise ValueError("Offset cannot exceed UInt16 samples")
        if period > 0 and offset + sample_count > period:
            raise ValueError(
                "The period of a Stimulus Waveform must be longer than its "
                "offset and waveform duration."
            )

        self.set_request(Packet(
            self.code,
            (sample_count + 3) * 2,
            ChecksumAlgorithmType.CRC8CCITT,
        ))
        self.request.insert_uint16(0, self.repeat)
        self.request.insert_uint16(2, offset)
        self.request.insert_uint16(4, period)

        index = 6
        for sample in self.samples[:sample_count]:
            sample = saturate(sample, -1.0, 1.0)
            value = int(saturate(int(sample * self.MAX_VALUE), -self.MAX_VALUE, self.MAX_VALUE))
            self.request.insert_int16(index, value)
            index += 2

    def __str__(self) -> str:
        return "[0x15] Set Waveform"
