import pytest

from labbench_comm.protocols.packet import (
    Packet,
    LengthEncodingType,
    ChecksumAlgorithmType,
    PacketFormatError,
)


def test_standard_packet_roundtrip():
    pkt = Packet(code=0x10, length=4)
    pkt.insert_uint16(0, 0x1234)
    pkt.insert_uint16(2, 0x5678)

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)

    assert parsed.code == 0x10
    assert parsed.length == 4
    assert parsed.get_uint16(0) == 0x1234
    assert parsed.get_uint16(2) == 0x5678


def test_extended_packet_with_checksum():
    pkt = Packet(
        code=0x20,
        length=2,
        checksum=ChecksumAlgorithmType.ADDITIVE,
    )

    pkt.address = 0x42
    pkt.insert_uint16(0, 0xABCD)

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)

    assert parsed.code == 0x20
    assert parsed.address == 0x42
    assert parsed.get_uint16(0) == 0xABCD


def test_checksum_validation_fails():
    pkt = Packet(
        code=0x30,
        length=1,
        checksum=ChecksumAlgorithmType.ADDITIVE,
    )
    pkt.insert_uint16(0, 0x01)

    raw = bytearray(pkt.to_bytes())
    raw[-1] ^= 0xFF  # corrupt checksum

    with pytest.raises(PacketFormatError):
        Packet.from_frame(bytes(raw))


def test_uint32_encoding():
    pkt = Packet(code=0x40, length=4)
    pkt.insert_uint32(0, 0xDEADBEEF)

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)

    assert parsed.get_uint32(0) == 0xDEADBEEF


def test_reverse_endianity():
    pkt = Packet(code=0x50, length=2)
    pkt.reverse_endianity = True
    pkt.insert_uint16(0, 0x1234)

    raw = pkt.to_bytes()
    parsed = Packet.from_frame(raw)
    parsed.reverse_endianity = True

    assert parsed.get_uint16(0) == 0x1234
