import asyncio
import time
from abc import ABC, abstractmethod
from typing import Optional, List

from labbench_comm.bus.bus_master import BusMaster
from labbench_comm.protocols.device_function import DeviceFunction
from labbench_comm.protocols.device_message import DeviceMessage
from labbench_comm.protocols.functions.device_identification import DeviceIdentification
from labbench_comm.protocols.functions.ping import Ping
from labbench_comm.protocols.error_codes import ErrorCode
from labbench_comm.protocols.exceptions import IncompatibleDeviceError


class Device(ABC):
    """
    Base class for all devices.

    A Device owns a BusMaster and defines:
    - compatibility checks
    - retry policy
    - common functions (ping, identification)
    - message handling
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self, bus: BusMaster) -> None:
        self.central = bus
        self.central.message_listener = self

        self.timeout_ms: int = 500
        self.retries: int = 1
        self.ping_enabled: bool = False

        self.current_address: Optional[int] = None

        self._functions: List[DeviceFunction] = []

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def is_open(self) -> bool:
        return self.central.is_open

    # ------------------------------------------------------------------
    # Function registration
    # ------------------------------------------------------------------

    @property
    def functions(self) -> List[DeviceFunction]:
        return self._functions

    def add_function(self, function: DeviceFunction) -> None:
        self._functions.append(function)

    def add_message(self, message: DeviceMessage) -> None:
        self.central.add_message(message)

    # ------------------------------------------------------------------
    # Ping
    # ------------------------------------------------------------------

    async def ping(self) -> int:
        """
        Ping the connected device.

        Returns the ping counter, or -1 on failure.
        """
        try:
            ping = self.create_ping()
            await self.execute(ping)
            return int(ping.count)
        except Exception:
            return -1

    def create_ping(self) -> DeviceFunction:
        return Ping()

    # ------------------------------------------------------------------
    # Identification
    # ------------------------------------------------------------------

    def create_identification_function(self) -> DeviceFunction:
        return DeviceIdentification()

    @abstractmethod
    def is_compatible(self, function: DeviceFunction) -> bool:
        """
        Determine whether the connected peripheral is compatible.
        """
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    async def open(self) -> None:
        if self.central.is_open:
            return
        await self.central.open()

    async def close(self) -> None:
        if not self.central.is_open:
            return
        await self.central.close()

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------

    async def execute(self, function: DeviceFunction) -> None:
        """
        Execute a DeviceFunction with retry handling.
        """
        if function is None:
            return

        last_error: Optional[Exception] = None

        for attempt in range(self.retries):
            try:
                start = time.monotonic()
                await self.central.execute(function, self.current_address)
                elapsed_ms = int((time.monotonic() - start) * 1000)
                function.transmission_time = elapsed_ms
                return
            except Exception as exc:
                last_error = exc
                if attempt == self.retries - 1:
                    raise

        if last_error:
            raise last_error

    async def send(self, message: DeviceMessage) -> None:
        await self.central.send(message, self.current_address)

    # ------------------------------------------------------------------
    # Message handlers
    # ------------------------------------------------------------------

    def get_error_string(self, error_code: int) -> str:
        """
        Convert protocol error codes to human-readable strings.
        """
        try:
            code = ErrorCode(error_code)
        except ValueError:
            return self.get_peripheral_error_string(error_code)

        if code is ErrorCode.NO_ERROR:
            return "No error (0x00)"
        if code is ErrorCode.UNKNOWN_FUNCTION_ERR:
            return "Unknown function (0x01)"
        if code is ErrorCode.INVALID_CONTENT_ERR:
            return "Invalid content (0x02)"

        return self.get_peripheral_error_string(error_code)

    @abstractmethod
    def get_peripheral_error_string(self, error_code: int) -> str:
        raise NotImplementedError

    # ------------------------------------------------------------------
    # Compatibility helper
    # ------------------------------------------------------------------

    async def identify_and_check(self) -> None:
        """
        Perform device identification and compatibility check.
        """
        ident = self.create_identification_function()
        await self.execute(ident)

        if not self.is_compatible(ident):
            raise IncompatibleDeviceError(str(ident))

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return "Generic Device"
