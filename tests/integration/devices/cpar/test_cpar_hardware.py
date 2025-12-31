import os
import asyncio
import pytest
import serial.tools.list_ports

from labbench_comm.serial.connection import PySerialIO
from labbench_comm.serial.async_serial_connection import AsyncSerialConnection
from labbench_comm.protocols.bus_central import BusCentral
from labbench_comm.devices.cpar.cpar_central import CPARplusCentral
from labbench_comm.protocols.functions.device_identification import DeviceIdentification


pytestmark = pytest.mark.asyncio

def get_first_serial_port() -> str:
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        pytest.skip("No serial ports available on this system")
    return ports[0].device


@pytest.mark.asyncio
@pytest.mark.cpar
async def test_cpar_device_identification():
    """
    Full hardware integration test.

    Verifies that:
    - serial port opens
    - device responds
    - DeviceIdentification works
    - compatibility check passes
    """

    port = get_first_serial_port()
    baudrate = 38400

    serial_io = PySerialIO(
        port=port,
        baudrate=baudrate
    )

    connection = AsyncSerialConnection(serial_io)
    bus = BusCentral(connection)
    device = CPARplusCentral(bus)

    # ---- Open connection ----
    await device.open()

    try:
        # ---- Execute identification ----
        ident = DeviceIdentification()
        await device.execute(ident)

        # ---- Assertions ----
        assert ident.manufacturer_id is not None
        assert ident.device_id is not None

        # Compatibility must pass
        assert device.is_compatible(ident)

    finally:
        await device.close()
