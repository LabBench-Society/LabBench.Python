from labbench_comm.protocols.packet import Packet

from labbench_comm.devices.lio.definitions import UINT32_MAX, saturate
from labbench_comm.devices.lio.functions.base import MAX_VOLTAGE, _LIOFunction


class SetVoltage(_LIOFunction):
    @property
    def code(self) -> int:
        return 0x18

    def __init__(self) -> None:
        super().__init__(request_length=4, response_length=0)
        self._voltage = 0.0

    @property
    def voltage(self) -> float:
        return self._voltage

    @voltage.setter
    def voltage(self, value: float) -> None:
        self._voltage = saturate(value, -MAX_VOLTAGE, MAX_VOLTAGE)

    def on_send(self) -> None:
        argument = self.voltage / MAX_VOLTAGE
        argument = UINT32_MAX * (argument + 1.0) / 2.0
        self.set_request(Packet(self.code, 4))
        self.request.insert_uint32(0, int(argument))

    def __str__(self) -> str:
        return "[0x18] SetVoltage"
