import pytest
import asyncio

import serial.tools.list_ports

from labbench_comm.serial.connection import PySerialIO
from labbench_comm.serial.async_serial_connection import AsyncSerialConnection
from labbench_comm.protocols.bus_central import BusCentral
from labbench_comm.protocols.device import Device
from labbench_comm.protocols.functions.device_identification import DeviceIdentification


# ----------------------------------------------------------------------
# Minimal concrete device for testing
# ----------------------------------------------------------------------

class IdentificationOnlyDevice(Device):
    def is_compatible(self, function) -> bool:
        return True

    def get_peripheral_error_string(self, error_code: int) -> str:
        return f"Peripheral error {error_code}"


# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def get_first_serial_port() -> str:
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        pytest.skip("No serial ports available on this system")
    return ports[0].device


# ----------------------------------------------------------------------
# Hardware integration test (Windows)
# ----------------------------------------------------------------------

@pytest.mark.asyncio
@pytest.mark.hardware
async def test_device_identification_hardware_windows():
    """
    Integration test that verifies a real device responds to
    DeviceIdentification over a physical serial connection.

    Assumes:
    - Windows
    - First available serial port
    """

    port = get_first_serial_port()
    baudrate = 115200

    serial_io = PySerialIO(
        port=port,
        baudrate=baudrate,
    )

    connection = AsyncSerialConnection(serial_io)
    bus = BusCentral(device=None, connection=connection)

    device = IdentificationOnlyDevice(bus)
    device.current_address = None  # set if your protocol requires addressing

    try:
        await device.open()

        ident = DeviceIdentification()
        await device.execute(ident)

        # ---------------- Assertions ----------------

        assert ident.manufacturer is not None
        assert ident.device is not None
        assert ident.version is not None

        assert len(ident.manufacturer) > 0
        assert len(ident.device) > 0

    finally:
        await device.close()
