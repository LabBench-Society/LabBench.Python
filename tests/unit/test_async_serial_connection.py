import pytest
import asyncio

from labbench_comm.protocols.destuffer import Destuffer
from labbench_comm.protocols.frame import Frame
from labbench_comm.serial.async_serial_connection import AsyncSerialConnection


class FakeSerialIO:
    def __init__(self):
        self._open = False
        self._rx = bytearray()
        self._tx = bytearray()

    def open(self):
        self._open = True

    def close(self):
        self._open = False

    @property
    def is_open(self):
        return self._open

    def write_bytes(self, data: bytes):
        self._tx.extend(data)

    def read_nonblocking(self, max_bytes: int):
        if not self._rx:
            return 0, b""

        data = self._rx[:max_bytes]
        del self._rx[:max_bytes]
        return len(data), bytes(data)

    # Test helper
    def inject_rx(self, data: bytes):
        self._rx.extend(data)


@pytest.mark.asyncio
async def test_async_serial_connection_reads():
    serial = FakeSerialIO()
    conn = AsyncSerialConnection(serial)

    received = []

    destuffer = Destuffer()
    destuffer.on_receive(lambda _, frame: received.append(frame))
    conn.attach_destuffer(destuffer)

    await conn.open()

    payload = b"\x01\x02"
    serial.inject_rx(Frame.encode(payload))

    await asyncio.sleep(0.01)

    assert received == [payload]

    await conn.close()


@pytest.mark.asyncio
async def test_reader_cancellation():
    serial = FakeSerialIO()
    conn = AsyncSerialConnection(serial)

    # ✅ Attach a minimal destuffer to satisfy invariants
    conn.attach_destuffer(Destuffer())

    await conn.open()
    await conn.close()

    assert not conn.is_open
