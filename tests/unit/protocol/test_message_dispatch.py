import pytest

from labbench_comm.devices.cpar.messages.status_message import StatusMessage
from labbench_comm.devices.cpar.messages.event_message import EventMessage
from labbench_comm.protocols.packet import Packet
from labbench_comm.devices.cpar.definitions import EventID


# ---------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------

class DummyListener:
    def __init__(self):
        self.status_called = False
        self.event_called = False
        self.received_status = None
        self.received_event = None

    def on_status_message(self, msg: StatusMessage):
        self.status_called = True
        self.received_status = msg

    def on_event_message(self, msg: EventMessage):
        self.event_called = True
        self.received_event = msg


class ListenerWithoutHandlers:
    """Listener that intentionally has no handlers."""
    pass


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

@pytest.mark.unittest
def test_status_message_dispatch_calls_correct_handler():
    packet = Packet(0x80, 22)
    msg = StatusMessage(packet)

    listener = DummyListener()

    msg.dispatch(listener)

    assert listener.status_called is True
    assert listener.received_status is msg
    assert listener.event_called is False

@pytest.mark.unittest
def test_event_message_dispatch_calls_correct_handler():
    packet = Packet(0x81, 1)
    packet.insert_byte(0, EventID.EVT_START_STIMULATION.value)
    msg = EventMessage(packet)

    listener = DummyListener()

    msg.dispatch(listener)

    assert listener.event_called is True
    assert listener.received_event is msg
    assert listener.status_called is False


@pytest.mark.unittest
def test_dispatch_does_not_fail_if_handler_missing():
    packet = Packet(0x80, 22)
    msg = StatusMessage(packet)

    listener = ListenerWithoutHandlers()

    # Should not raise
    msg.dispatch(listener)


@pytest.mark.unittest
def test_dispatch_does_not_call_wrong_handler():
    packet = Packet(0x81, 1)
    packet.insert_byte(0, EventID.EVT_STOP_STIMULATION.value)
    msg = EventMessage(packet)

    listener = DummyListener()

    msg.dispatch(listener)

    assert listener.event_called is True
    assert listener.status_called is False


@pytest.mark.unittest
def test_multiple_messages_dispatch_independently():
    status_packet = Packet(0x80, 22)
    event_packet = Packet(0x81, 1)

    status_msg = StatusMessage(status_packet)
    event_msg = EventMessage(event_packet)

    listener = DummyListener()

    status_msg.dispatch(listener)
    event_msg.dispatch(listener)

    assert listener.status_called is True
    assert listener.event_called is True
    assert listener.received_status is status_msg
    assert listener.received_event is event_msg
