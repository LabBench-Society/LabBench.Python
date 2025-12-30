import asyncio
from typing import Optional

from labbench_comm.serial.base import SerialIO
from labbench_comm.protocols.destuffer import Destuffer


class AsyncSerialConnection:
    """
    Async transport wrapper around a non-blocking SerialIO.
    """

    def __init__(self, serial_io: SerialIO) -> None:
        self._io = serial_io
        self._destuffer: Optional[Destuffer] = None

        self._reader_task: Optional[asyncio.Task] = None
        self._running = False

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def attach_destuffer(self, destuffer: Destuffer) -> None:
        self._destuffer = destuffer

    async def open(self) -> None:
        self._io.open()
        self._running = True
        self._reader_task = asyncio.create_task(self._reader_loop())

    async def close(self) -> None:
        self._running = False

        if self._reader_task:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except asyncio.CancelledError:
                pass

        self._io.close()

    @property
    def is_open(self) -> bool:
        return self._io.is_open

    # ------------------------------------------------------------------
    # I/O
    # ------------------------------------------------------------------

    async def write_bytes(self, data: bytes) -> None:
        await asyncio.to_thread(self._io.write_bytes, data)

    # ------------------------------------------------------------------
    # Background reader
    # ------------------------------------------------------------------

    async def _reader_loop(self) -> None:
        try:
            while self._running:
                n, data = self._io.read_nonblocking(1024)
                if n and self._destuffer:
                    self._destuffer.add_bytes(data)

                # Yield to the event loop (no busy loop)
                await asyncio.sleep(0)
        except asyncio.CancelledError:
            pass
