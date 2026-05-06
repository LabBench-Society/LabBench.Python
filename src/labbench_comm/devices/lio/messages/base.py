from __future__ import annotations

import re

from labbench_comm.protocols.device_message import DeviceMessage
from labbench_comm.protocols.exceptions import InvalidMessageError
from labbench_comm.protocols.message_dispatcher import MessageDispatcher
from labbench_comm.protocols.packet import Packet


def _checked_message_packet(
    message_name: str,
    code: int,
    length: int,
    packet: Packet | None,
) -> Packet | None:
    if packet is None:
        return None
    if packet.length != length:
        raise InvalidMessageError(
            f"A received {message_name} does not have a length of {length}"
        )
    if packet.code != code:
        raise InvalidMessageError(
            f"A received {message_name} does not have code 0x{code:02X}"
        )
    return packet


def _handler_name(message_name: str) -> str:
    stem = message_name.removesuffix("Message")
    snake = re.sub(r"(?<!^)(?=[A-Z])", "_", stem).lower()
    return f"on_{snake}_message"


class _LIOMessage(DeviceMessage):
    MESSAGE_LENGTH = 0

    def __init__(self, packet: Packet | None = None) -> None:
        checked = _checked_message_packet(
            self.__class__.__name__,
            self.code,
            self.MESSAGE_LENGTH,
            packet,
        )
        if checked is not None:
            super().__init__(checked)
        else:
            super().__init__(length=self.MESSAGE_LENGTH)

    def create_dispatcher(self) -> MessageDispatcher:
        return MessageDispatcher(self.code, lambda p: self.__class__(p))

    def dispatch(self, listener) -> None:
        handler_name = _handler_name(self.__class__.__name__)
        if hasattr(listener, handler_name):
            getattr(listener, handler_name)(self)
