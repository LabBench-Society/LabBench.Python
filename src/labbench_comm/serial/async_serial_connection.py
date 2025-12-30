import asyncio


class AsyncSerialConnection(AsyncConnection):

    def __init__(self, serial_io):
        self._io = serial_io
        self._destuffer = None
        self._reader_task = None
        self._running = False

    def attach_destuffer(self, destuffer):
        self._destuffer = destuffer

    async def open(self):
        self._io.open()
        self._running = True
        self._reader_task = asyncio.create_task(self._reader_loop())

    async def close(self):
        self._running = False
        if self._reader_task:
            self._reader_task.cancel()
        self._io.close()

    @property
    def is_open(self):
        return self._io.is_open

    async def write_bytes(self, data: bytes):
        await asyncio.to_thread(self._io.write_bytes, data)

    async def _reader_loop(self):
        while self._running:
            n, data = self._io.read_nonblocking(1024)
            if n and self._destuffer:
                self._destuffer.add_bytes(data)
            await asyncio.sleep(0)
