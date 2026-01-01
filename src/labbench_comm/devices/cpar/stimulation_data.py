from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class StimulationSample:
    actual_pressure_01: float
    target_pressure_01: float
    final_pressure_01: float

    actual_pressure_02: float
    target_pressure_02: float
    final_pressure_02: float

    vas_score: float
    final_vas_score: float


class StimulationData:
    """
    Collected data from a single stimulation cycle.
    """

    def __init__(self) -> None:
        self.samples: List[StimulationSample] = []

    def add_sample(self, sample: StimulationSample) -> None:
        self.samples.append(sample)

    def __len__(self) -> int:
        return len(self.samples)
