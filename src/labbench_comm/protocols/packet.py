from __future__ import annotations

from enum import IntEnum
import struct


# ----------------------------------------------------------------------
# Enums
# ----------------------------------------------------------------------

class LengthEncodingType(IntEnum):
    UINT8 = 0x00
    UINT16 = 0x01
    UINT32 = 0x02


class ChecksumAlgorithmType(IntEnum):
    NONE = 0x00
    ADDITIVE = 0x04
    CRC8_CCITT = 0x08


# ----------------------------------------------------------------------
# Exceptions
# ----------------------------------------------------------------------

class PacketError(Exception):
    pass


class PacketFormatError(PacketError):
    pass


# ----------------------------------------------------------------------
# Checksum utilities (self-contained)
# ----------------------------------------------------------------------

def additive_checksum(data: bytes) -> int:
    return sum(data) & 0xFF


def crc8_ccitt(data: bytes) -> int:
    crc = 0x00
    for b in data:
        crc ^= b
        for _ in range(8):
            if crc & 0x80:
                crc = ((crc << 1) ^ 0x07) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
    return crc


# ----------------------------------------------------------------------
# Packet
# ----------------------------------------------------------------------

class Packet:
    """
    Protocol packet with optional extended header, address, and checksum.
    Faithful port of LabBench.IO.Packet.
    """

    def __init__(
        self,
        code: int,
        length: int,
        checksum: ChecksumAlgorithmType = ChecksumAlgorithmType.NONE,
    ) -> None:
        self._code = code
        self._length = length
        self._length_encoding = self._get_length_encoding(length)
        self._checksum_type = checksum

        self.address: int = 0
        self.reverse_endianity: bool = False

        self._checksum: int = 0
        self._data = bytearray(length)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def code(self) -> int:
        return self._code

    @property
    def is_function(self) -> bool:
        return self._code < 128

    @property
    def length(self) -> int:
        return self._length

    @property
    def length_encoding(self) -> LengthEncodingType:
        return self._length_encoding

    @property
    def empty(self) -> bool:
        return self._length == 0

    @property
    def address_enabled(self) -> bool:
        return self.address != 0

    @property
    def checksum_algorithm(self) -> ChecksumAlgorithmType:
        return self._checksum_type

    @property
    def extended(self) -> bool:
        if self.address_enabled:
            return True
        if self._checksum_type != ChecksumAlgorithmType.NONE:
            return True
        if self._length_encoding in (
            LengthEncodingType.UINT16,
            LengthEncodingType.UINT32,
        ):
            return True
        return self._length >= 128

    # ------------------------------------------------------------------
    # Parsing
    # ------------------------------------------------------------------

    @classmethod
    def from_frame(cls, frame: bytes) -> Packet:
        if frame is None or len(frame) < 2:
            raise PacketFormatError("Frame is null or too short")

        code = frame[0]
        fmt = frame[1]

        if fmt < 128:
            length = fmt
            pkt = cls(code, length)
            offset = 2
        else:
            length_enc = LengthEncodingType(fmt & 0x03)
            checksum_type = ChecksumAlgorithmType(fmt & 0x0C)
            addr_enabled = bool(fmt & 0x10)

            length = cls._decode_length(frame, length_enc)
            pkt = cls(code, length, checksum_type)

            offset = 2 + cls._length_size(length_enc)
            if addr_enabled:
                pkt.address = frame[offset]
                offset += 1

        pkt._data[:] = frame[offset : offset + pkt.length]

        if pkt.extended and pkt.checksum_algorithm != ChecksumAlgorithmType.NONE:
            expected = frame[offset + pkt.length]
            actual = (
                additive_checksum(frame[:-1])
                if pkt.checksum_algorithm == ChecksumAlgorithmType.ADDITIVE
                else crc8_ccitt(frame[:-1])
            )

            if expected != actual:
                raise PacketFormatError(
                    f"Checksum mismatch (expected {expected}, got {actual})"
                )

            pkt._checksum = expected

        return pkt

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_bytes(self) -> bytes:
        if not self.extended:
            return bytes([self._code, self._length]) + bytes(self._data)

        header_len = 2 + self._length_size(self._length_encoding)
        if self.address_enabled:
            header_len += 1

        total_len = header_len + self._length
        if self._checksum_type != ChecksumAlgorithmType.NONE:
            total_len += 1

        frame = bytearray(total_len)
        frame[0] = self._code
        frame[1] = (
            0x80
            | self._length_encoding
            | self._checksum_type
            | (0x10 if self.address_enabled else 0x00)
        )

        self._encode_length(frame)

        offset = 2 + self._length_size(self._length_encoding)
        if self.address_enabled:
            frame[offset] = self.address
            offset += 1

        frame[offset : offset + self._length] = self._data

        if self._checksum_type == ChecksumAlgorithmType.ADDITIVE:
            self._checksum = additive_checksum(frame[:-1])
            frame[-1] = self._checksum
        elif self._checksum_type == ChecksumAlgorithmType.CRC8_CCITT:
            self._checksum = crc8_ccitt(frame[:-1])
            frame[-1] = self._checksum

        return bytes(frame)

    # ------------------------------------------------------------------
    # Data access helpers
    # ------------------------------------------------------------------

    def insert_uint16(self, pos: int, value: int) -> None:
        self._serialize(pos, struct.pack("<H", value))

    def insert_uint32(self, pos: int, value: int) -> None:
        self._serialize(pos, struct.pack("<I", value))

    def get_uint16(self, pos: int) -> int:
        return struct.unpack("<H", self._deserialize(pos, 2))[0]

    def get_uint32(self, pos: int) -> int:
        return struct.unpack("<I", self._deserialize(pos, 4))[0]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _get_length_encoding(length: int) -> LengthEncodingType:
        if length > 0xFFFF:
            return LengthEncodingType.UINT32
        if length > 0xFF:
            return LengthEncodingType.UINT16
        return LengthEncodingType.UINT8

    @staticmethod
    def _length_size(enc: LengthEncodingType) -> int:
        return {LengthEncodingType.UINT8: 1,
                LengthEncodingType.UINT16: 2,
                LengthEncodingType.UINT32: 4}[enc]

    @staticmethod
    def _decode_length(frame: bytes, enc: LengthEncodingType) -> int:
        if enc == LengthEncodingType.UINT8:
            return frame[2]
        if enc == LengthEncodingType.UINT16:
            return struct.unpack_from("<H", frame, 2)[0]
        if enc == LengthEncodingType.UINT32:
            return struct.unpack_from("<I", frame, 2)[0]
        raise PacketFormatError("Invalid length encoding")

    def _encode_length(self, frame: bytearray) -> None:
        struct.pack_into(
            {LengthEncodingType.UINT8: "<B",
             LengthEncodingType.UINT16: "<H",
             LengthEncodingType.UINT32: "<I"}[self._length_encoding],
            frame,
            2,
            self._length,
        )

    def _serialize(self, pos: int, data: bytes) -> None:
        if self.reverse_endianity:
            data = data[::-1]
        self._data[pos : pos + len(data)] = data

    def _deserialize(self, pos: int, size: int) -> bytes:
        data = bytes(self._data[pos : pos + size])
        return data[::-1] if self.reverse_endianity else data
