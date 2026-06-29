import argparse
import asyncio

import labbench_comm.devices.lio as lio

from common import add_port_argument, attach_print_callbacks, open_lio


async def main() -> None:
    parser = argparse.ArgumentParser(description="Monitor LIO response port messages.")
    add_port_argument(parser)
    parser.add_argument("--duration", type=float, default=20.0)
    parser.add_argument("--sample-period", type=int, default=200)
    args = parser.parse_args()

    async with open_lio(args.port) as device:
        attach_print_callbacks(device)

        print("Configuring response port requirements")
        required = lio.SetRequiredDevices()
        required.port01 = lio.ResponseDevice.DEVICE_RESPONSE_INPUT
        required.port01_subclass = lio.ResponseSubClass.DEVICE_SUBCLASS_NONE
        required.port02 = lio.ResponseDevice.DEVICE_NONE
        required.port02_subclass = lio.ResponseSubClass.DEVICE_SUBCLASS_NONE
        await device.execute(required)

        print("Configuring signal sample periods")
        for port in [lio.ResponsePort.RESPONSE_PORT01, lio.ResponsePort.RESPONSE_PORT02]:
            sample_period = lio.SetSignalSamplePeriod()
            sample_period.port = port
            sample_period.period = args.sample_period
            await device.execute(sample_period)

        print(f"Monitoring for {args.duration:0.1f}s")
        await asyncio.sleep(args.duration)


if __name__ == "__main__":
    asyncio.run(main())
