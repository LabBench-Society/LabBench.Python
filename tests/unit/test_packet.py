import pytest

from labbench_comm.protocols.packet import (
    Packet,
    LengthEncodingType,
    ChecksumAlgorithmType,
)
from labbench_comm.protocols.exceptions import (
    PacketFormatError,
    ChecksumError,
)


# ----------------------------------------------------------------------
# Construction & basic properties
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_packet_basic_properties():
    pkt = Packet(code=0x10, length=4)

    assert pkt.code == 0x10
    assert pkt.length == 4
    assert not pkt.empty
    assert pkt.is_function
    assert pkt.address == 0
    assert not pkt.address_enabled
    assert pkt.checksum_algorithm == ChecksumAlgorithmType.NONE


# ----------------------------------------------------------------------
# Insert / Get primitives
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_insert_and_get_primitives():
    pkt = Packet(code=0x01, length=12)

    pkt.insert_byte(0, 0xAA)
    pkt.insert_bool(1, True)
    pkt.insert_uint16(2, 0x1234)
    pkt.insert_int16(4, -123)
    pkt.insert_uint32(6, 0xCAFEBABE)

    assert pkt.get_byte(0) == 0xAA
    assert pkt.get_bool(1) is True
    assert pkt.get_uint16(2) == 0x1234
    assert pkt.get_int16(4) == -123
    assert pkt.get_uint32(6) == 0xCAFEBABE


# ----------------------------------------------------------------------
# String handling
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_insert_and_get_string():
    pkt = Packet(code=0x01, length=16)

    pkt.insert_string(0, 16, "HELLO")
    assert pkt.get_string(0, 16) == "HELLO"

    pkt.insert_string(0, 16, "A" * 32)
    assert pkt.get_string(0, 16) == "A" * 16


# ----------------------------------------------------------------------
# Endian reversal
# ----------------------------------------------------------------------

@pytest.mark.unittest
def test_reverse_endianity():
    pkt = Packet(code=0x01, length=4)
    pkt.reverse_endianity = True

    pkt.insert_uint32(0, 0x11223344)
    assert pkt.get_uint32(0) == 0x11223344


# ----------------------------------------------------------------------
# Standard frame round-trip
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_standard_frame_roundtrip():
    pkt = Packet(code=0x02, length=3)
    pkt.insert_byte(0, 1)
    pkt.insert_byte(1, 2)
    pkt.insert_byte(2, 3)

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)

    assert parsed.code == pkt.code
    assert parsed.length == pkt.length
    assert parsed.get_byte(0) == 1
    assert parsed.get_byte(1) == 2
    assert parsed.get_byte(2) == 3


# ----------------------------------------------------------------------
# Extended frame with address
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_extended_frame_with_address():
    pkt = Packet(code=0x20, length=2)
    pkt.address = 0x42
    pkt.insert_byte(0, 0xAA)
    pkt.insert_byte(1, 0xBB)

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)

    assert parsed.address == 0x42
    assert parsed.get_byte(0) == 0xAA
    assert parsed.get_byte(1) == 0xBB


# ----------------------------------------------------------------------
# Length encoding variants
# ----------------------------------------------------------------------
@pytest.mark.unittest
@pytest.mark.parametrize(
    "length,expected_encoding",
    [
        (10, LengthEncodingType.UINT8),
        (300, LengthEncodingType.UINT16),
        (70000, LengthEncodingType.UINT32),
    ],
)
def test_length_encoding_variants(length, expected_encoding):
    pkt = Packet(code=0x01, length=length)
    assert pkt._length_encoding == expected_encoding

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)
    assert parsed.length == length


# ----------------------------------------------------------------------
# Additive checksum
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_additive_checksum_roundtrip():
    pkt = Packet(
        code=0x10,
        length=4,
        checksum=ChecksumAlgorithmType.ADDITIVE,
    )
    pkt.insert_uint32(0, 0x01020304)

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)

    assert parsed.get_uint32(0) == 0x01020304


# ----------------------------------------------------------------------
# CRC8 checksum
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_crc8_checksum_roundtrip():
    pkt = Packet(
        code=0x10,
        length=4,
        checksum=ChecksumAlgorithmType.CRC8CCITT,
    )
    pkt.insert_uint32(0, 0xDEADBEEF)

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)

    assert parsed.get_uint32(0) == 0xDEADBEEF


# ----------------------------------------------------------------------
# Checksum validation failure
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_checksum_validation_error():
    pkt = Packet(
        code=0x10,
        length=1,
        checksum=ChecksumAlgorithmType.ADDITIVE,
    )
    pkt.insert_byte(0, 0x01)

    raw = bytearray(pkt.to_bytes())
    raw[-1] ^= 0xFF  # corrupt checksum

    with pytest.raises(ChecksumError):
        Packet.from_frame(bytes(raw))


# ----------------------------------------------------------------------
# Packet format errors
# ----------------------------------------------------------------------
@pytest.mark.unittest
def test_packet_format_error_on_short_frame():
    with pytest.raises(PacketFormatError):
        Packet.from_frame(b"\x01")

@pytest.mark.unittest
def test_packet_format_error_on_none():
    with pytest.raises(PacketFormatError):
        Packet.from_frame(None)
