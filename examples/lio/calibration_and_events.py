import argparse
from datetime import date
import asyncio

import labbench_comm.devices.lio as lio

from common import add_port_argument, open_lio


async def main() -> None:
    parser = argparse.ArgumentParser(description="Read LIO calibration and event records.")
    add_port_argument(parser)
    parser.add_argument("--write-event", action="store_true")
    args = parser.parse_args()

    async with open_lio(args.port) as device:
        print("Reading calibration records")
        for calibrator in [
            lio.CalibratorID.ID_RSP01_CALIBRATOR,
            lio.CalibratorID.ID_RSP02_CALIBRATOR,
        ]:
            record = lio.ReadCalibration()
            record.calibrator = calibrator
            await device.execute(record)
            print(
                f"{calibrator.name}: "
                f"valid={record.valid_marker} "
                f"a={record.a:0.6f} "
                f"b={record.b:0.6f} "
                f"maximum={record.maximum} "
                f"checksum=0x{record.checksum:02X}"
            )

        print("Reading event records")
        for event_type in [
            lio.DeviceEventType.BUILD_EVENT,
            lio.DeviceEventType.CALIBRATION_EVENT,
        ]:
            event = lio.GetEvent()
            event.device_event = event_type
            await device.execute(event)
            print(
                f"{event_type.name}: "
                f"valid={event.valid} "
                f"id={event.event_id} "
                f"date={event.date.isoformat()} "
                f"text={event.text}"
            )

        if args.write_event:
            print("Writing calibration event metadata")
            event = lio.SetEvent()
            event.device_event = lio.DeviceEventType.CALIBRATION_EVENT
            event.valid = True
            event.event_id = 1
            event.date = date.today()
            event.text = "Updated from Python example"
            await device.execute(event)


if __name__ == "__main__":
    asyncio.run(main())
