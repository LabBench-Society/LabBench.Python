import argparse
from contextlib import asynccontextmanager

import serial.tools.list_ports

from labbench_comm.protocols.bus_central import BusCentral
from labbench_comm.serial.async_serial_connection import AsyncSerialConnection
from labbench_comm.serial.connection import PySerialIO
import labbench_comm.devices.lio as lio


BAUDRATE = 57600


def add_port_argument(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--port",
        default=None,
        help="Serial port to use. Defaults to the first available serial port.",
    )


def get_serial_port(port: str | None = None) -> str:
    if port:
        return port

    ports = list(serial.tools.list_ports.comports())
    if not ports:
        raise RuntimeError("No serial ports available")

    return ports[0].device


def create_lio(port: str | None = None) -> lio.LIOCentral:
    serial_io = PySerialIO(
        port=get_serial_port(port),
        baudrate=BAUDRATE,
    )
    connection = AsyncSerialConnection(serial_io)
    return lio.LIOCentral(BusCentral(connection))


@asynccontextmanager
async def open_lio(port: str | None = None):
    device = create_lio(port)
    await device.open()
    try:
        yield device
    finally:
        await device.close()


def attach_print_callbacks(device: lio.LIOCentral) -> None:
    device.status_received.append(print_status)
    device.event_received.append(print_event)
    device.signal_received.append(print_signal)
    device.button_received.append(print_button)
    device.trigger_received.append(print_trigger)
    device.threshold_received.append(print_threshold)
    device.analog_input_received.append(print_analog_input)


def print_status(device: lio.LIOCentral, msg: lio.StatusMessage) -> None:
    print(
        f"STATUS state={msg.state.name:<18} "
        f"port1={msg.port01.name:<18} "
        f"port2={msg.port02.name:<18} "
        f"power={msg.power} "
        f"error={msg.error.name}"
    )


def print_event(device: lio.LIOCentral, msg: lio.EventMessage) -> None:
    print(f"EVENT {msg.event.name}")


def print_signal(device: lio.LIOCentral, msg: lio.SignalMessage) -> None:
    print(
        f"SIGNAL port={msg.port.name:<15} "
        f"device={msg.device.name:<18} "
        f"value={msg.value:0.3f} "
        f"voltage={msg.voltage:0.3f}V "
        f"target={msg.target:0.3f}"
    )


def print_button(device: lio.LIOCentral, msg: lio.ButtonMessage) -> None:
    print(
        f"BUTTON port={msg.port.name:<15} "
        f"button={msg.button} "
        f"state={msg.state} "
        f"time={msg.time}ms"
    )


def print_trigger(device: lio.LIOCentral, msg: lio.TriggerMessage) -> None:
    print(
        f"TRIGGER port={msg.port.name:<15} "
        f"code={msg.trigger_code} "
        f"time={msg.time}ms"
    )


def print_threshold(device: lio.LIOCentral, msg: lio.ThresholdMessage) -> None:
    print(
        f"THRESHOLD port={msg.port.name:<15} "
        f"value={msg.value:0.3f} "
        f"response_time={msg.response_time}ms"
    )


def print_analog_input(device: lio.LIOCentral, msg: lio.AnalogInputMessage) -> None:
    print(
        f"ANALOG pin={msg.pin} "
        f"value={msg.value:0.3f} "
        f"voltage={msg.voltage:0.3f}V"
    )
