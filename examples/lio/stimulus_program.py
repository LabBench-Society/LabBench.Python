import argparse
import asyncio

import labbench_comm.devices.lio as lio

from common import add_port_argument, attach_print_callbacks, open_lio


async def main() -> None:
    parser = argparse.ArgumentParser(description="Run a simple LIO stimulus program.")
    add_port_argument(parser)
    parser.add_argument("--repeat", type=int, default=1)
    parser.add_argument("--settle", type=float, default=5.0)
    args = parser.parse_args()

    async with open_lio(args.port) as device:
        attach_print_callbacks(device)

        print("Clearing existing programs")
        await device.execute(lio.ClearPrograms())

        print("Uploading stimulus program")
        program = lio.SetStimulusProgram(lio.UpdateRate.CLK1000Hz)
        program.set(0.0, 100.0)
        program.inc(2.0, 500.0)
        program.nop(250.0)
        program.dec(-2.0, 500.0)
        program.set(0.0, 100.0)
        await device.execute(program)

        print("Starting program")
        start = lio.Start()
        start.trigger = lio.InputTriggerSource.TRIG_NONE
        start.rate = lio.UpdateRate.CLK1000Hz
        start.reset_on_completion = True
        start.restart_on_completion = False
        start.stimulus_program_repeat = args.repeat
        await device.execute(start)

        print(f"Waiting {args.settle:0.1f}s for messages")
        await asyncio.sleep(args.settle)


if __name__ == "__main__":
    asyncio.run(main())
