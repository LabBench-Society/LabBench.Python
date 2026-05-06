import argparse
import asyncio

from labbench_comm.protocols.functions.device_identification import DeviceIdentification
import labbench_comm.devices.lio as lio

from common import add_port_argument, attach_print_callbacks, open_lio


async def main() -> None:
    parser = argparse.ArgumentParser(description="Open and identify a LabBench I/O device.")
    add_port_argument(parser)
    parser.add_argument(
        "--listen",
        type=float,
        default=3.0,
        help="Seconds to print incoming messages after identification.",
    )
    args = parser.parse_args()

    async with open_lio(args.port) as device:
        attach_print_callbacks(device)

        print("Pinging device")
        count = await device.ping()
        print(f"Ping count: {count}")

        print("Reading device identification")
        ident = DeviceIdentification()
        await device.execute(ident)
        print(
            f"Manufacturer={ident.manufacturer} "
            f"Device={ident.device} "
            f"ID={ident.device_id} "
            f"Version={ident.version} "
            f"Serial={ident.serial_number}"
        )

        if not device.is_compatible(ident):
            raise RuntimeError(f"Connected device is not compatible with {lio.LIOCentral}")

        print(f"Listening for {args.listen:0.1f}s")
        await asyncio.sleep(args.listen)


if __name__ == "__main__":
    asyncio.run(main())
