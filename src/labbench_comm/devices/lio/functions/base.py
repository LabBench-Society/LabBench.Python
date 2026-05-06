from labbench_comm.protocols.device_function import DeviceFunction
from labbench_comm.protocols.function_dispatcher import FunctionDispatcher


EVENT_TEXT_SIZE = 64
EVENT_RECORD_SIZE = 9 + EVENT_TEXT_SIZE
CALIBRATION_RECORD_SIZE = 12
CALIBRATION_VALID_MARKER = 0xC9
CALIBRATION_Q = 12
MAX_VOLTAGE = 10.0


class _LIOFunction(DeviceFunction):
    def create_dispatcher(self) -> FunctionDispatcher:
        return FunctionDispatcher(self.code, self.__class__)

    def dispatch(self, listener):
        return listener.accept(self)
