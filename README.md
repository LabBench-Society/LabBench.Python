# labbench-comm

**labbench-comm** is an asynchronous Python framework for communicating with LabBench hardware devices over serial connections.

It provides a testable protocol stack for deterministic device communication, with typed device functions, messages, packet framing, checksums, and concrete device implementations.

## Features

- Async-first communication using `asyncio`
- Serial transport support using `pyserial`
- Protocol primitives for frames, packets, stuffing, checksums, dispatch, and device functions
- Typed device-specific functions and messages
- Hardware-oriented examples for supported LabBench devices
- Unit tests plus optional hardware integration tests

## Supported Devices

- **CPAR+**: pressure stimulation device support, including waveform control and status/event messages
- **LabBench I/O (LIO)**: response ports, trigger I/O, analog input/status messages, waveform output, stimulus programs, calibration/event records

## Requirements

- Python **3.12+**
- Windows, Linux, or macOS
- Serial access to compatible LabBench hardware for hardware examples and integration tests

## Installation

Install the package:

```bash
pip install labbench-comm
```

The Python import package is named `labbench_comm`:

```python
import labbench_comm.devices.lio as lio
import labbench_comm.devices.cpar as cpar
```

## Quick Start

```python
import asyncio

from labbench_comm.protocols.bus_central import BusCentral
from labbench_comm.serial.async_serial_connection import AsyncSerialConnection
from labbench_comm.serial.connection import PySerialIO
import labbench_comm.devices.lio as lio


async def main() -> None:
    serial_io = PySerialIO(port="COM3", baudrate=57600)
    connection = AsyncSerialConnection(serial_io)
    bus = BusCentral(connection)
    device = lio.LIOCentral(bus)

    async with device:
        count = await device.ping()
        print("Ping:", count)


asyncio.run(main())
```

## Examples

Examples live in [`examples/`](examples/README.md).

LIO examples include device identification, input monitoring, analog reads, direct voltage output, stimulus programs, waveforms, trigger sequences, and calibration/event records.

Some examples directly drive hardware outputs. Review the script and connected setup before running output-driving examples such as:

```bash
python examples/lio/manual_voltage.py --port COM3 --voltage 1.0
python examples/lio/stimulus_program.py --port COM3
```

## Development Setup

This repository uses a `src/` layout. Install it into the same environment that will run tests or examples:

```bash
python -m pip install -e .[dev]
```

Run unit tests:

```bash
python -m pytest -m unittest -v
```

Build and verify distributions:

```bash
python -m build
twine check dist/*
```

## Project Status

This project is in alpha. APIs may change while device support and protocol coverage mature.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, testing guidance, and contribution expectations.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
