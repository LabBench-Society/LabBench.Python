import asyncio
import serial.tools.list_ports

from labbench_comm.serial.connection import PySerialIO
from labbench_comm.serial.async_serial_connection import AsyncSerialConnection
from labbench_comm.protocols.bus_central import BusCentral
from labbench_comm.protocols.exceptions import FunctionNotAcknowledgedError
from plotting import plot_stimulation_data
import labbench_comm.devices.cpar as cpar

def get_first_serial_port() -> str:
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        raise RuntimeError("No ports availabel")
    
    return ports[0].device


async def main() -> None:
    serial_io = PySerialIO(
        port=get_first_serial_port(),
        baudrate=38400
    )

    connection = AsyncSerialConnection(serial_io)
    bus = BusCentral(connection)
    device = cpar.CPARplusCentral(bus)
    try:

        # ---- Open connection ----
        print("Opening device")
        await device.open()

        print("Pinging device")
        await device.ping()

        print("Clearing waveforms")
        await device.execute(cpar.ClearWaveformPrograms())

        print("Setting pressure waveform")
        
        waveformFunction = cpar.SetWaveformProgram()
        waveformFunction.instructions = [
            cpar.WaveformInstruction.step(50,1),
            cpar.WaveformInstruction.step(0, 1)
        ]
        waveformFunction.repeat = 10
        waveformFunction.channel = 0
        await device.execute(waveformFunction)

        print("Start pinging")
        await device.start_ping()

        print("Starting waveform")
        startFunction = cpar.StartStimulation()
        startFunction.criterion = cpar.StopCriterion.STOP_CRITERION_ON_BUTTON_PRESSED
        startFunction.external_trigger = False
        startFunction.outlet01 = cpar.DeviceChannelID.CH01
        startFunction.outlet02 = cpar.DeviceChannelID.NONE
        await device.execute(startFunction)

        print("Wait for stimulation to complete")
        data = await device.wait_for_stimulation_complete(0.5)

        print("Stimulation complete")
        await device.stop_ping()

        plot_stimulation_data(data, "Temporal Summation")

    finally:
        await device.close()

if __name__ == "__main__":
    asyncio.run(main())
