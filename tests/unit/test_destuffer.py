import pytest

from labbench_comm.protocols.destuffer import Destuffer, Frame


def test_single_frame_roundtrip():
    destuffer = Destuffer()
    received = []

    def on_receive(_, payload: bytes):
        received.append(payload)

    destuffer.on_receive(on_receive)

    payload = b"\x01\x02\x03\x04"
    framed = (
        bytes([Frame.DLE, Frame.STX])
        + payload
        + bytes([Frame.DLE, Frame.ETX])
    )

    destuffer.add_bytes(framed)

    assert received == [payload]


def test_dle_escaping():
    destuffer = Destuffer()
    received = []

    destuffer.on_receive(lambda _, p: received.append(p))

    payload = bytes([0x01, Frame.DLE, 0x02])
    framed = (
        bytes([Frame.DLE, Frame.STX])
        + bytes([0x01, Frame.DLE, Frame.DLE, 0x02])
        + bytes([Frame.DLE, Frame.ETX])
    )

    destuffer.add_bytes(framed)

    assert received == [payload]


def test_chunked_input():
    destuffer = Destuffer()
    received = []

    destuffer.on_receive(lambda _, p: received.append(p))

    framed = bytes([
        Frame.DLE, Frame.STX,
        0x10, 0x20,
        Frame.DLE, Frame.ETX
    ])

    # Feed one byte at a time (like serial)
    for b in framed:
        destuffer.add_byte(b)

    assert received == [b"\x10\x20"]


def test_invalid_sequence_is_discarded():
    destuffer = Destuffer()
    received = []

    destuffer.on_receive(lambda _, p: received.append(p))

    # Missing STX
    destuffer.add_bytes(bytes([Frame.DLE, 0x00, 0x01]))

    # Valid frame after corruption
    valid = (
        bytes([Frame.DLE, Frame.STX])
        + b"\xAA"
        + bytes([Frame.DLE, Frame.ETX])
    )

    destuffer.add_bytes(valid)

    assert received == [b"\xAA"]
