import argparse
import asyncio
import math

import labbench_comm.devices.lio as lio

from common import add_port_argument, attach_print_callbacks, open_lio


def sine_samples(count: int, amplitude: float) -> list[float]:
    return [
        amplitude * math.sin(2.0 * math.pi * i / count)
        for i in range(count)
    ]


async def main() -> None:
    parser = argparse.ArgumentParser(description="Upload and run a LIO waveform.")
    add_port_argument(parser)
    parser.add_argument("--samples", type=int, default=100)
    parser.add_argument("--amplitude", type=float, default=0.5)
    parser.add_argument("--repeat", type=int, default=3)
    parser.add_argument("--settle", type=float, default=5.0)
    args = parser.parse_args()

    async with open_lio(args.port) as device:
        attach_print_callbacks(device)

        print("Clearing existing programs")
        await device.execute(lio.ClearPrograms())

        print("Uploading waveform")
        waveform = lio.SetWaveform()
        waveform.rate = lio.UpdateRate.CLK1000Hz
        waveform.repeat = args.repeat
        waveform.offset = 0.0
        waveform.period = 0.0
        waveform.samples.extend(sine_samples(args.samples, args.amplitude))
        await device.execute(waveform)

        print("Starting waveform")
        start = lio.Start()
        start.trigger = lio.InputTriggerSource.TRIG_NONE
        start.rate = waveform.rate
        start.reset_on_completion = True
        start.restart_on_completion = False
        await device.execute(start)

        print(f"Waiting {args.settle:0.1f}s for messages")
        await asyncio.sleep(args.settle)


if __name__ == "__main__":
    asyncio.run(main())
