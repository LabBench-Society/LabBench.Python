# labbench_comm/core/exceptions.py

class LabBenchCommError(Exception):
    """Base exception for all labbench-comm errors."""


class SerialError(LabBenchCommError):
    """Generic serial communication failure."""


class SerialTimeoutError(SerialError):
    """Read or write timed out."""


class SerialConnectionError(SerialError):
    """Serial port could not be opened or was lost."""


class SerialClosedError(SerialError):
    """Operation attempted on a closed serial connection."""
