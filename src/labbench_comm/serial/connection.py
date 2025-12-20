# labbench_comm/serial/connection.py

from __future__ import annotations
from typing import Optional, Tuple

import serial
from serial import SerialException

from labbench_comm.serial.base import SerialIO
from labbench_comm.core.exceptions import (
    SerialError,
    SerialClosedError,
    SerialConnectionError,
)


class PySerialIO(SerialIO):
    """
    Robust SerialIO implementation using pyserial.

    Non-blocking reads are controlled entirely through
    pyserial's `in_waiting` buffer and timeout=0.
    """

    def __init__(
        self,
        port: str,
        baudrate: int = 115200,
        write_timeout: float = 1.0,
        *,
        bytesize: int = serial.EIGHTBITS,
        parity: str = serial.PARITY_NONE,
        stopbits: int = serial.STOPBITS_ONE,
    ) -> None:
        """
        The read timeout is *not* used — read_nonblocking never blocks.
        """
        self._port = port
        self._baudrate = baudrate
        self._write_timeout = write_timeout

        self._bytesize = bytesize
        self._parity = parity
        self._stopbits = stopbits

        self._serial: Optional[serial.Serial] = None

    # -------------------- Lifecycle -------------------- #

    def open(self) -> None:
        """Open the serial port (no-op if already open)."""
        if self.is_open:
            return

        try:
            self._serial = serial.Serial(
                port=self._port,
                baudrate=self._baudrate,
                timeout=0.0,  # non-blocking reads
                write_timeout=self._write_timeout,
                bytesize=self._bytesize,
                parity=self._parity,
                stopbits=self._stopbits,
            )
        except SerialException as exc:
            raise SerialConnectionError(
                f"Failed to open serial port {self._port}"
            ) from exc

    def close(self) -> None:
        """Close the port, freeing the handle."""
        if self._serial is not None:
            try:
                self._serial.close()
            finally:
                self._serial = None

    @property
    def is_open(self) -> bool:
        return self._serial is not None and self._serial.is_open

    def _require_open(self) -> serial.Serial:
        if not self.is_open or self._serial is None:
            raise SerialClosedError("Serial port is not open")
        return self._serial

    # -------------------- I/O -------------------- #

    def write_bytes(self, data: bytes) -> None:
        """
        Write raw bytes and flush.
        Raises on short write or OS error.
        """
        ser = self._require_open()

        try:
            written = ser.write(data)
            ser.flush()
        except SerialException as exc:
            raise SerialConnectionError("Serial write failed") from exc

        if written != len(data):
            raise SerialError(
                f"Partial write ({written}/{len(data)} bytes)"
            )

    def read_nonblocking(self, max_bytes: int) -> Tuple[int, bytes]:
        """
        Read up to max_bytes from the input buffer without blocking.
        """

        ser = self._require_open()

        try:
            available = ser.in_waiting
        except SerialException as exc:
            raise SerialConnectionError(
                "Failed to query serial input buffer"
            ) from exc

        if available <= 0:
            return 0, b""

        to_read = min(available, max_bytes)

        try:
            data = ser.read(to_read)
        except SerialException as exc:
            raise SerialConnectionError("Non-blocking read failed") from exc

        return len(data), data
