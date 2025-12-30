"""
Protocol- and device-level exceptions.
"""


# ----------------------------------------------------------------------
# Base exception
# ----------------------------------------------------------------------

class LabBenchError(Exception):
    """Base class for LabBench protocol errors."""
    pass


# ----------------------------------------------------------------------
# Device / protocol exceptions
# ----------------------------------------------------------------------

class IncompatibleDeviceError(LabBenchError):
    """Raised when a device is incompatible with the expected protocol."""
    pass


class InvalidMasterRequestError(LabBenchError):
    """Raised when a master sends an invalid request."""
    pass


class InvalidMessageError(LabBenchError):
    """Raised when a received message is invalid."""
    pass


class InvalidSlaveResponseError(LabBenchError):
    """Raised when a slave response is invalid."""
    pass


class PacketFormatError(LabBenchError):
    """Raised when a packet is malformed or cannot be parsed."""
    pass


class PeripheralNotRespondingError(LabBenchError):
    """Raised when a peripheral fails to respond."""
    pass


class FunctionNotAcknowledgedError(LabBenchError):
    """
    Raised when a function is explicitly not acknowledged by the device.
    """

    @property
    def error_code(self) -> int:
        """
        Attempt to parse the error code from the exception message.

        Returns:
            int: Parsed error code, or -1 if unavailable.
        """
        try:
            return int(str(self))
        except (ValueError, TypeError):
            return -1
