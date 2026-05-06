# Examples

These examples demonstrate hardware workflows for supported LabBench devices.

Install the package in editable mode before running examples:

```bash
python -m pip install -e .[dev]
```

Most scripts accept `--port COMx`. If no port is provided, scripts use the first serial port reported by `pyserial`.

## Safety

Some examples directly control hardware outputs such as pressure, voltage, stimulus programs, waveforms, and trigger lines. Verify the connected hardware, output cabling, and expected signal levels before running output-driving scripts.

## LIO Examples

Run from the repository root:

```bash
python examples/lio/device_overview.py --port COM3
```

| Script | Purpose |
| --- | --- |
| `lio/device_overview.py` | Open the device, ping, read identification, and print incoming messages |
| `lio/monitor_response_ports.py` | Configure response ports and print status/signal/button/trigger/threshold messages |
| `lio/read_inputs.py` | Read analog channels and trigger interface status |
| `lio/manual_voltage.py` | Set a direct output voltage, then stop and clear programs |
| `lio/stimulus_program.py` | Upload and start a simple stimulus program |
| `lio/waveform_output.py` | Upload and start a waveform output |
| `lio/trigger_sequence.py` | Configure and run a trigger sequence |
| `lio/calibration_and_events.py` | Read calibration and event records, optionally write event metadata |

## CPAR+ Examples

| Script | Purpose |
| --- | --- |
| `cpar/stimulus_response.py` | Run a repeated pressure stimulus-response workflow |
| `cpar/temporal_summation.py` | Run a temporal summation pressure workflow |
| `cpar/conditioned_pain_modulation.py` | Run a two-channel conditioned pain modulation workflow |
| `cpar/plotting.py` | Plot CPAR stimulation data |
