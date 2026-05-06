import argparse
import asyncio

import labbench_comm.devices.lio as lio

from common import add_port_argument, attach_print_callbacks, open_lio


async def main() -> None:
    parser = argparse.ArgumentParser(description="Configure and run a LIO trigger sequence.")
    add_port_argument(parser)
    parser.add_argument("--settle", type=float, default=5.0)
    args = parser.parse_args()

    async with open_lio(args.port) as device:
        attach_print_callbacks(device)

        print("Configuring trigger timing source")
        timing = lio.SetTimingSource()
        timing.port = lio.ResponsePort.RESPONSE_PORT01
        timing.source = lio.TimingSource.SOURCE_GENERATOR_START
        await device.execute(timing)

        arming = lio.SetTriggerArmingPeriod()
        arming.port = lio.ResponsePort.RESPONSE_PORT01
        arming.period = 200
        await device.execute(arming)

        print("Sending manual trigger")
        trigger = lio.SetTrigger()
        trigger.trigger = True
        trigger.stimulus_trigger = True
        trigger.trigger_code = 1
        await device.execute(trigger)

        print("Uploading trigger sequence")
        sequence = lio.SetTriggerSequence()
        sequence.rate = lio.UpdateRate.CLK1000Hz
        sequence.add(lio.TriggerInstruction(1, True, True), duration=10.0)
        sequence.add(lio.TriggerInstruction(0, False, False), duration=100.0)
        sequence.add(lio.TriggerInstruction(2, True, False), duration=10.0)
        await device.execute(sequence)

        print("Starting trigger sequence")
        start = lio.Start()
        start.trigger = lio.InputTriggerSource.TRIG_NONE
        start.rate = sequence.rate
        start.trigger_sequence_repeat = 1
        start.reset_on_completion = True
        await device.execute(start)

        print(f"Waiting {args.settle:0.1f}s for messages")
        await asyncio.sleep(args.settle)


if __name__ == "__main__":
    asyncio.run(main())
