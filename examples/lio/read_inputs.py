import argparse
import asyncio

import labbench_comm.devices.lio as lio

from common import add_port_argument, attach_print_callbacks, open_lio


CHANNELS = [
    lio.AnalogChannel.RES1_RATING,
    lio.AnalogChannel.RES1_DETECT,
    lio.AnalogChannel.TRIG_S13,
    lio.AnalogChannel.TRIG_S25,
    lio.AnalogChannel.SUPPLY_VOLTAGE,
]


async def main() -> None:
    parser = argparse.ArgumentParser(description="Read LIO analog and interface inputs.")
    add_port_argument(parser)
    parser.add_argument("--listen", type=float, default=5.0)
    args = parser.parse_args()

    async with open_lio(args.port) as device:
        attach_print_callbacks(device)

        print("Reading selected analog channels")
        for channel in CHANNELS:
            function = lio.GetAnalogSignal()
            function.channel = channel
            await device.execute(function)
            print(f"{channel.name:<16} raw={function.value}")

        print("Reading trigger interface status")
        status = lio.GetInterfaceStatus()
        await device.execute(status)
        print(
            f"low={status.low_byte_level.name} "
            f"high={status.high_byte_level.name} "
            f"valid={status.valid} "
            f"logic={status.logic.name}"
        )

        print(f"Listening for input messages for {args.listen:0.1f}s")
        await asyncio.sleep(args.listen)


if __name__ == "__main__":
    asyncio.run(main())
