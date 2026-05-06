import argparse
import asyncio

import labbench_comm.devices.lio as lio

from common import add_port_argument, attach_print_callbacks, open_lio


async def main() -> None:
    parser = argparse.ArgumentParser(description="Set a direct LIO output voltage.")
    add_port_argument(parser)
    parser.add_argument("--voltage", type=float, default=1.0)
    parser.add_argument("--hold", type=float, default=2.0)
    args = parser.parse_args()

    async with open_lio(args.port) as device:
        attach_print_callbacks(device)

        print(f"Setting voltage to {args.voltage:0.3f}V")
        voltage = lio.SetVoltage()
        voltage.voltage = args.voltage
        await device.execute(voltage)

        await asyncio.sleep(args.hold)

        print("Stopping and clearing programs")
        stop = lio.Stop()
        stop.reset_programs = True
        await device.execute(stop)
        await device.execute(lio.ClearPrograms())


if __name__ == "__main__":
    asyncio.run(main())
