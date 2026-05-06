import pytest

from labbench_comm.devices.lio import LIOCentral
from labbench_comm.protocols.bus_central import BusCentral
from labbench_comm.protocols.functions.device_identification import DeviceIdentification
from labbench_comm.protocols.functions.ping import Ping
from labbench_comm.protocols.manufacturer import Manufacturer


class FakeConnection:
    def __init__(self) -> None:
        self.destuffer = None

    def attach_destuffer(self, destuffer) -> None:
        self.destuffer = destuffer

    @property
    def is_open(self) -> bool:
        return False

    async def open(self) -> None:
        pass

    async def close(self) -> None:
        pass

    async def write_bytes(self, data: bytes) -> None:
        pass


def make_device() -> LIOCentral:
    return LIOCentral(BusCentral(FakeConnection()))


def make_identification(
    manufacturer_id: Manufacturer,
    device_id: int,
) -> DeviceIdentification:
    ident = DeviceIdentification()
    ident.manufacturer_id = manufacturer_id
    ident.device_id = device_id
    return ident


@pytest.mark.unittest
def test_lio_central_import_and_constructor_defaults():
    device = make_device()

    assert isinstance(device, LIOCentral)
    assert device.baudrate == 57600
    assert device.retries == 3
    assert str(device) == "LIO Device"


@pytest.mark.unittest
def test_lio_central_is_compatible_for_lio_identification():
    device = make_device()
    ident = make_identification(Manufacturer.InventorsWay, 2)

    assert device.is_compatible(ident)


@pytest.mark.unittest
def test_lio_central_rejects_wrong_manufacturer():
    device = make_device()
    ident = make_identification(Manufacturer.Detectronic, 2)

    assert not device.is_compatible(ident)


@pytest.mark.unittest
def test_lio_central_rejects_wrong_device_id():
    device = make_device()
    ident = make_identification(Manufacturer.InventorsWay, 4)

    assert not device.is_compatible(ident)


@pytest.mark.unittest
def test_lio_central_rejects_non_identification_function():
    device = make_device()

    assert not device.is_compatible(Ping())


@pytest.mark.unittest
def test_lio_central_unknown_peripheral_error_string():
    device = make_device()

    assert device.get_peripheral_error_string(17) == "Unknown LIO error (17)"
