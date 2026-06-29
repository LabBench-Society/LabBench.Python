# Interface Design Description: LabBench I/O (LIO) ECP Interface

## Scope

This document describes the implemented Embedded Communication Protocol (ECP) functions and messages handled by the LabBench I/O (LIO) firmware communication peripheral.

Evidence was taken from code only, primarily:

- `Firmware/LIOLite.Firmware/source/srv/comm/ecp/PeripheralHandler.c`
- `Firmware/LIOLite.Firmware/source/srv/comm/ecp/Packet.c`
- `Firmware/LIOLite.Firmware/include/sys/SystemConfig.h`
- `Firmware/LIOLite.Firmware/source/sys/System.c`
- Firmware headers under `Firmware/LIOLite.Firmware/include/`
- CommLib packet field definitions under `CommLib/LIO.CommLib/`

## Protocol Framing

[IMPLEMENTED] The firmware receives and transmits ECP frames over `SerialPort`.

Standard frame format transmitted by the firmware:

| Field | Size | Value |
| --- | ---: | --- |
| DLE | 1 | `0xFF` |
| STX | 1 | `0xF1` |
| Code | 1 | Function or message code |
| Length | 1 | Payload length in bytes |
| Data | `Length` | Payload bytes |
| DLE | 1 | `0xFF` |
| ETX | 1 | `0xF2` |

[IMPLEMENTED] Any payload byte equal to `DLE` (`0xFF`) is byte-stuffed as `DLE DLE`.

[IMPLEMENTED] The firmware accepts standard request frames and a subset of extended request frames. Extended request frames support `uint8` and `uint16` length encodings, optional address byte, no checksum, or CRC-8-CCITT checksum. `uint32` length encoding and additive checksum are not implemented.

[IMPLEMENTED] Firmware responses are transmitted as standard frames without an outbound checksum.

[IMPLEMENTED] Multi-byte numeric fields are little-endian. The `GET_ENDIANNESS` function returns `uint16` value `1`.

## Common Response Rules

[IMPLEMENTED] Successful command acknowledgement uses the original function code and a zero-length payload:

| Field | Value |
| --- | --- |
| Code | Request function code |
| Length | `0` |

[IMPLEMENTED] Functions that return data use the original function code and the documented response payload.

[IMPLEMENTED] Negative acknowledgement uses code `0x00`, length `1`, and one payload byte containing an `EcpError` value.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Error code |

[IMPLEMENTED] Unknown function codes return `ECP_UNKNOWN_FUNCTION_ERR`.

[IMPLEMENTED] CRC-8-CCITT request checksum mismatch returns `ECP_CHECKSUM_ERR` and discards the received request.

## Functions

### Summary

| Code | Name | Request length | Response on success |
| ---: | --- | ---: | --- |
| `0x01` | `DEVICE_IDENTIFICATION` | 0 | 64-byte identification payload |
| `0x02` | `ECP_PING` | 0 | 4-byte request counter |
| `0x03` | `GET_ENDIANNESS` | 0 | 2-byte endian marker |
| `0x12` | `SET_INDICATORS` | 6 | ACK |
| `0x13` | `SET_STIMULUS_PROGRAM` | `7 * n` | ACK |
| `0x14` | `SET_TRIGGER_SEQUENCE` | `5 * n` | ACK |
| `0x15` | `SET_WAVEFORM` | `6 + 2 * n` | ACK |
| `0x16` | `START` | 8 | ACK |
| `0x17` | `SET_TRIGGER` | 3 | ACK |
| `0x18` | `SET_VOLTAGE_OUT` | 4 | ACK |
| `0x19` | `CLEAR_PROGRAMS` | 0 | ACK |
| `0x20` | `STOP` | 1 | ACK |
| `0x21` | `SET_REQUIRED_DEVICES` | 4 | ACK |
| `0x22` | `SET_TIMING_SOURCE` | 2 | ACK |
| `0x23` | `SET_TRIGGER_ARMING_PERIOD` | 3 | ACK |
| `0x24` | `SET_SIGNAL_SAMPLE_PERIOD` | 3 | ACK |
| `0x25` | `GET_ANALOG_VALUE` | 1 | 2-byte ADC value |
| `0x32` | `SET_TRIGGER_LEVEL` | 3 | ACK |
| `0x40` | `WRITE_SERIAL_NUMBER` | 2 expected | ACK |
| `0x41` | `WRITE_CALIBRATION` | 13 | ACK |
| `0x42` | `READ_CALIBRATION` | 1 expected | 12-byte calibration record |
| `0x46` | `GET_EVENT` | 1 | 73-byte event record |
| `0x47` | `SET_EVENT` | 74 | ACK |
| `0x48` | `RESET` | 0 | ACK, then reset wait loop |
| `0x49` | `SET_INTERFACE_LOGIC` | 3 | ACK |
| `0x50` | `GET_INTERFACE_STATUS` | 0 | 4-byte interface status |

### `DEVICE_IDENTIFICATION` (`0x01`)

Request length: 0.

Response length: 64.

| Offset | Type | Meaning | Implemented source |
| ---: | --- | --- | --- |
| 0 | `uint32` | Manufacturer ID | `MANUFACTURER_ID` = `1` |
| 4 | `uint16` | Device type | `DEVICE_TYPE` = `2` |
| 6 | `uint32` | Serial number, or `0` when invalid | `system.serialNumber` |
| 10 | `uint8` | Major revision | `3` |
| 11 | `uint8` | Minor revision | `0` |
| 12 | `uint8` | Patch revision | `0` |
| 13 | `uint8` | Engineering revision | `1` |
| 14 | `uint16` | Program checksum | `system.checksum` |
| 16 | `char[24]` | Manufacturer name, zero-padded | `Inventors Way ApS` |
| 40 | `char[24]` | Device name, zero-padded | `LabBench I/O` |

Description:

[IMPLEMENTED] Returns static product identity fields and live device identity fields. The firmware reports the manufacturer ID, device type, firmware revision constants, and the program checksum calculated during system initialization. It reports the EEPROM serial number only when the loaded serial record is marked valid; otherwise it reports serial number `0`. The command does not modify device state.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `ECP_PING` (`0x02`)

Request length: 0.

Response length: 4.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint32` | Peripheral request counter |

[IMPLEMENTED] The counter is incremented before dispatching each valid request, so the first processed request returns `1`.

Description:

[IMPLEMENTED] Provides a minimal liveness and request-dispatch check. The returned counter reflects how many valid request frames have reached `PeripheralHandler_Run` and entered the switch dispatcher since initialization. Requests rejected earlier by packet parsing or checksum validation are not counted by this handler path.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `GET_ENDIANNESS` (`0x03`)

Request length: 0.

Response length: 2.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint16` | Endian marker, always `1` |

Description:

[IMPLEMENTED] Allows a host to confirm the firmware's multi-byte field byte order. The firmware sends the `uint16` value `1` using its native packet send routine; a host that receives bytes as `01 00` can interpret subsequent multi-byte fields as little-endian. The command does not modify device state.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `SET_INDICATORS` (`0x12`)

Request length: 6.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint8` | LED bitfield, bits 0 through 7 map to indicators D1 through D8 |
| 2 | `uint32` | Duration |

Description:

[IMPLEMENTED] Sets the monochrome indicator state for a connected response device on the selected response port. The LED bitfield is forwarded to `Response_SetMonochromeIndicators`; the current implementation accepts this operation only for detected sensor devices and returns a wrong-device error for other response-device types. The `duration` field is parsed by the peripheral handler, but the analyzed `Response_SetMonochromeIndicators` path forwards only the LED state to `SensorDevice_SetIndicators`.

On success, returns ACK.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`. Response-device failures are mapped through `ResponseStatus` as described in [Response Status Error Mapping](#response-status-error-mapping).

### `SET_STIMULUS_PROGRAM` (`0x13`)

Request length: `7 * n`, where `0 <= n <= 256`.

| Per-instruction offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `Opcode` |
| 1 | `uint32` | Operand |
| 5 | `uint16` | Duration in generator update cycles |

Description:

[IMPLEMENTED] Loads a stimulus instruction program into `programMemory` and marks it as the active program definition for later generator starts. The command is accepted only while the system is idle, preventing replacement of the program while output generation or pending trigger operation is active. Each instruction is consumed by `Program_CalculateUpdate` when the generator runs. A zero-length request is accepted by the code path and results in `PRG_NONE`, which clears the stored stimulus program type without clearing the trigger sequence.

[IMPLEMENTED] The command only initializes the stored program; it does not start output generation. A later `START` command calls `Program_Start`, which begins execution from the first instruction and uses the `START` stimulus repeat count.

Instruction byte layout:

| Byte offset | Size | Field | Encoding |
| ---: | ---: | --- | --- |
| `0 + 7*i` | 1 | Opcode | One of the values in the opcode table below |
| `1 + 7*i` | 4 | Operand | Little-endian unsigned raw signal value or raw per-update delta |
| `5 + 7*i` | 2 | Duration | Little-endian `uint16` count of generator update cycles |

Supported opcodes:

| Opcode | Name | Operand meaning | Duration meaning |
| ---: | --- | --- | --- |
| `0x00` | `NOP` | Ignored by firmware; conventionally send `0` | Keeps the current signal value for the requested number of update cycles |
| `0x02` | `INC` | Unsigned raw increment added to the current signal on each active update cycle | Number of update cycles over which the increment is applied |
| `0x04` | `DEC` | Unsigned raw decrement subtracted from the current signal on each active update cycle | Number of update cycles over which the decrement is applied |
| `0x06` | `SET` | Unsigned raw absolute signal value assigned to the current signal when the instruction is loaded | Keeps the assigned value until the instruction duration expires |

[IMPLEMENTED] The firmware does not reject undefined opcode values. During execution, an undefined opcode behaves like `NOP` for signal generation because only `SET`, `INC`, and `DEC` have explicit actions. Hosts should use only the four opcode values listed above.

Timing and update rate:

[IMPLEMENTED] `SET_STIMULUS_PROGRAM` does not carry an update-rate field. The host must compute instruction durations and ramp operands for the same `UpdateRate` that will later be passed to `START`. The firmware interprets `duration` only as update cycles.

Use these relationships when constructing requests:

```text
duration_cycles = duration_seconds * update_rate_hz
duration_ms     = duration_cycles * 1000 / update_rate_hz
```

The firmware consumes the integer `uint16` value in the packet. CommLib computes cycles as `duration_ms * update_rate_hz / 1000`, clamps to `0..65535`, and casts to `UInt16`.

Raw signal value:

[IMPLEMENTED] The program engine stores the current stimulus as an unsigned 32-bit raw signal. `MIDPOINT` is `2147483647`. Values below `MIDPOINT` drive DAC channel 0; values above `MIDPOINT` drive DAC channel 1; `MIDPOINT` is the zero-output point.

CommLib encodes a requested voltage in the nominal `-10 V` to `+10 V` range as:

```text
raw_signal = uint32((clamp(voltage_v, -10, +10) / 10 + 1) * UInt32.MaxValue / 2)
```

Useful raw values:

| Intended level | Raw operand | Little-endian bytes |
| --- | ---: | --- |
| `-10 V` nominal full scale | `0` / `0x00000000` | `00 00 00 00` |
| `0 V` nominal midpoint | `2147483647` / `0x7FFFFFFF` | `FF FF FF 7F` |
| `+10 V` nominal full scale | `4294967295` / `0xFFFFFFFF` | `FF FF FF FF` |

Raw ramp operands:

[IMPLEMENTED] `INC` and `DEC` do not use volts directly. They add or subtract the raw operand once per generator update while the instruction is active. Addition saturates at `UInt32.MaxValue`; subtraction saturates at `0`.

For a desired positive ramp slope:

```text
inc_operand = uint32((UInt32.MaxValue / 2) * (slope_v_per_ms / 10) * (1000 / update_rate_hz))
```

For a desired negative ramp slope, send `DEC` with a positive decrement magnitude:

```text
dec_operand = uint32((UInt32.MaxValue / 2) * (abs(slope_v_per_ms) / 10) * (1000 / update_rate_hz))
```

CommLib's `DEC(double value, double duration)` path expects `value` to be negative; positive `DEC` arguments are encoded as `0`.

Execution model:

[IMPLEMENTED] `Program_Start` resets the program counter and initializes the current signal to `defaultOutputVoltage`, which defaults to `MIDPOINT` and can be changed with `SET_VOLTAGE_OUT`. The first instruction is loaded when the generator prepares the first sample.

[IMPLEMENTED] On each program calculation, the firmware first applies the active instruction if its remaining duration counter is greater than zero. `INC` adds the operand, `DEC` subtracts the operand, and other opcodes leave the signal unchanged in this per-cycle step. The firmware then decrements the remaining duration counter. If the counter reaches zero, the firmware immediately loads following instructions until it finds an instruction with a non-zero duration or reaches the end of the program. A loaded `SET` updates the signal immediately. A zero-duration instruction does not by itself produce a held output sample; a zero-duration `SET` can establish a signal value for a following non-zero-duration instruction.

[IMPLEMENTED] When the program reaches the end, `programRepeat` from `START` controls repetition. If more repeats remain, the firmware resets the program counter and current signal to `defaultOutputVoltage` before starting the next repeat. If no repeats remain, it marks the program inactive and returns the signal to `defaultOutputVoltage`.

Construction guidance:

- Use `SET` for absolute levels.
- Use `NOP` to hold the current level without changing it.
- Use `SET` followed by `INC` or `DEC` to start a ramp from a known level.
- Append a `NOP` after an `INC` or `DEC` ramp when the final ramp value must be held.
- Keep each instruction exactly 7 bytes and keep the total request length a multiple of 7.
- Use an extended ECP frame for programs whose payload length is `128` bytes or larger; this firmware interprets a second frame byte with its high bit set as an extended-frame control byte, not as a standard length.

Example: hold the nominal zero-output level for 100 ms at `CLK1000Hz`.

```text
update_rate_hz = 1000
duration_cycles = 100 ms * 1000 Hz / 1000 = 100 = 0x0064
instruction = SET, raw_signal(0 V), duration 100
bytes = 06 FF FF FF 7F 64 00
```

On success, initializes `PRG_PROGRAM` with `n` instructions and returns ACK.

Implemented constraints:

- System state must be `STATE_IDLE`.
- Request length must be a multiple of 7.
- Instruction count must be at most `MAXIMAL_NUMBER_OF_INSTRUCTIONS` (`256`).

Possible handler errors:

- `ECP_ATTEMPT_TO_SET_PROGRAM_WHILE_SYSTEM_IS_NOT_IDLE_ERR`
- `ECP_INVALID_LENGTH_OF_STIMULUS_PROGRAM_ERR`
- `ECP_STIMULUS_PROGRAM_IS_TOO_LONG_ERR`

### `SET_TRIGGER_SEQUENCE` (`0x14`)

Request length: `5 * n`, where `0 <= n <= 128`.

| Per-trigger offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Trigger output bitfield: bit 0 = trigger output, bit 1 = stimulus trigger output |
| 1 | `uint16` | Trigger code |
| 3 | `uint16` | Duration in generator update cycles |

Description:

[IMPLEMENTED] Loads a trigger-output sequence into `triggerMemory` and marks it as the active trigger sequence definition for later generator starts. The command is accepted only while the system is idle. A zero-length request is accepted by the code path and creates a sequence with `triggerSize = 0`; `Trigger_Start` will not activate trigger generation for an empty sequence.

[IMPLEMENTED] The command only initializes the stored trigger sequence; it does not start trigger output generation.

Trigger record byte layout:

| Byte offset | Size | Field | Encoding |
| ---: | ---: | --- | --- |
| `0 + 5*i` | 1 | Trigger output bitfield | Bit 0 = `TRIGOUT`, bit 1 = `STIM_TRIG`; other bits are ignored by the generator |
| `1 + 5*i` | 2 | Trigger code | Little-endian `uint16` value for the 16-bit interface output code |
| `3 + 5*i` | 2 | Duration | Little-endian `uint16` count of generator update cycles |

Output bitfield:

| Bit | Mask | Meaning when set | Meaning when clear |
| ---: | ---: | --- | --- |
| 0 | `0x01` | Drive the trigger output active/high | Drive the trigger output inactive/low |
| 1 | `0x02` | Drive the stimulus-trigger output active/high | Drive the stimulus-trigger output inactive/low |

[IMPLEMENTED] The generator tests only `triggerOut & 0x01` and `triggerOut & 0x02`. Hosts should send only the low two bits unless a future firmware revision defines additional bits.

Trigger code output:

[IMPLEMENTED] The `code` field is copied into `currentTriggerState.code` when the record is loaded. On each generator interrupt, the low byte is written to the low interface byte and the high byte is written to the high interface byte. With positive interface logic, the firmware writes the code bits directly. With negative interface logic, the firmware writes the bitwise inverse of each byte. The output is then latched with the trigger latch clock.

[IMPLEMENTED] Outside an active trigger sequence, the firmware uses `defaultTriggerState`, which is configured by `SET_TRIGGER`. When a sequence finishes, the trigger state returns to that default trigger output bitfield and default trigger code.

Timing and update rate:

[IMPLEMENTED] `SET_TRIGGER_SEQUENCE` does not carry an update-rate field. The host must compute trigger durations for the same `UpdateRate` that will later be passed to `START`. The firmware interprets `duration` only as update cycles.

Use these relationships when constructing requests:

```text
duration_cycles = duration_seconds * update_rate_hz
duration_ms     = duration_cycles * 1000 / update_rate_hz
```

The firmware consumes the integer `uint16` value in the packet. CommLib computes cycles as `duration_ms * update_rate_hz / 1000`, clamps to `1..65535`, and casts to `UInt16`. The firmware itself does not reject `0`; however, hosts should send a duration of at least `1` for each trigger record because the generator loads records when its internal duration counter is zero.

Execution model:

[IMPLEMENTED] `Trigger_Start` is called by `START` and activates the loaded sequence only when the trigger type is `TRIG_SEQUENCE` and the sequence size is non-zero. It resets the sequence index to the first record, resets the duration counter, initializes the current trigger state from `defaultTriggerState`, and stores the `START` trigger sequence repeat count.

[IMPLEMENTED] When the generator prepares an update and the trigger duration counter is zero, it loads the next trigger record, copies that record's bitfield and code into `currentTriggerState`, advances the sequence index, and advances the memory address by 5 bytes. If the duration counter is greater than zero, it decrements the counter after the current record is selected. The selected trigger state is then copied into the generator update structure for the next hardware output update.

[IMPLEMENTED] When the sequence reaches the end, the repeat count from `START` controls repetition. A repeat count of `0` or `1` results in one sequence execution. If more repeats remain, the firmware resets the sequence index and address and immediately starts the next repeat. If no repeats remain, it marks trigger generation inactive and restores `currentTriggerState` from `defaultTriggerState`.

[IMPLEMENTED] Trigger sequence generation can run at the same time as a stimulus program or waveform. The final generator update combines the stimulus-program analog output fields with the current trigger-sequence output fields. If no stimulus program is active but a trigger sequence is active, the trigger sequence still causes generator updates.

Construction guidance:

- Treat each trigger record as a complete output state, not as an edge command.
- Add one record for each interval where the trigger outputs or 16-bit code must remain stable.
- Use `SET_TRIGGER` before `START` to define the idle/default trigger state used before the sequence starts and after it finishes.
- Use the same update rate for duration calculation that will be used in `START`.
- Keep each trigger record exactly 5 bytes and keep the total request length a multiple of 5.
- Use an extended ECP frame for sequences whose payload length is `128` bytes or larger; this firmware interprets a second frame byte with its high bit set as an extended-frame control byte, not as a standard length.

Example: drive `TRIGOUT` high, `STIM_TRIG` low, and output code `0x1234` for 10 ms at `CLK1000Hz`.

```text
update_rate_hz = 1000
duration_cycles = 10 ms * 1000 Hz / 1000 = 10 = 0x000A
trigger bitfield = 0x01
trigger code = 0x1234
record bytes = 01 34 12 0A 00
```

Example: generate a 5 ms trigger pulse on `TRIGOUT` and then return to code `0x0000` for 20 ms at `CLK1000Hz`.

```text
record 1: TRIGOUT high,  code 0x0001, duration 5  -> 01 01 00 05 00
record 2: TRIGOUT low,   code 0x0000, duration 20 -> 00 00 00 14 00
payload = 01 01 00 05 00 00 00 00 14 00
```

On success, initializes `TRIG_SEQUENCE` with `n` triggers and returns ACK.

Implemented constraints:

- System state must be `STATE_IDLE`.
- Request length must be a multiple of 5.
- Trigger count must be at most `TRIGGER_SEQUENCE_LENGTH` (`128`).

Possible handler errors:

- `ECP_ATTEMPT_TO_SET_TRIGGER_SEQUENCE_WHILE_SYSTEM_IS_NOT_IDLE_ERR`
- `ECP_INVALID_LENGTH_OF_TRIGGER_SEQUENCE_ERR`
- `ECP_TRIGGER_SEQUENCE_TOO_LONG_ERR`

### `SET_WAVEFORM` (`0x15`)

Request length: `6 + 2 * n`, where `0 <= n <= 1000`.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint16` | Wave repeat count |
| 2 | `uint16` | Wave offset in samples |
| 4 | `uint16` | Wave period in samples; when `0`, firmware uses `offset + sample count` |
| 6 | `int16[n]` | Signed waveform samples |

Description:

[IMPLEMENTED] Loads a sampled waveform into `programMemory` and marks it as the active waveform definition for later generator starts. The first three `uint16` values configure waveform repeat count, initial offset in samples, and period in samples. The remaining signed samples are converted during generation into the two DAC channels: negative values drive channel 0 with their absolute magnitude, positive values drive channel 1, and zero drives both waveform channels to zero. A request with only the 6-byte header and no samples is accepted by the code path and results in `PRG_NONE`, which clears the stored stimulus waveform/program type without clearing the trigger sequence.

[IMPLEMENTED] If the period field is `0`, `Program_Initialize` sets the period to `offset + sample count`. If the period is non-zero, it must be long enough to contain both the offset and the waveform samples. The command only initializes the stored waveform; it does not start output generation.

Waveform byte layout:

| Byte offset | Size | Field | Encoding |
| ---: | ---: | --- | --- |
| 0 | 2 | Repeat count | Little-endian `uint16` loaded into `waveRepeat` |
| 2 | 2 | Offset | Little-endian `uint16` count of leading zero-output samples before the first waveform sample |
| 4 | 2 | Period | Little-endian `uint16` count of samples in one waveform period; `0` means `offset + sample count` |
| `6 + 2*i` | 2 | Sample `i` | Little-endian signed `int16` sample |

Sample encoding:

[IMPLEMENTED] Each sample is a signed 16-bit raw value. The firmware uses the sign to select the DAC side and the magnitude as the DAC value:

| Sample value | Firmware output |
| --- | --- |
| Negative | `ch0 = -sample`, `ch1 = 0` |
| Zero | `ch0 = 0`, `ch1 = 0` |
| Positive | `ch0 = 0`, `ch1 = sample` |

[IMPLEMENTED] The firmware does not clamp sample magnitude in `SET_WAVEFORM`; it copies the received `int16` values into program memory and later casts their magnitudes to `uint16`. Hosts should keep waveform sample magnitudes in the DAC range used by CommLib, `-4095..4095`.

CommLib encodes normalized samples as:

```text
raw_sample = int16(clamp(sample_normalized, -1, +1) * 4095)
```

Useful sample values:

| Intended sample | Raw sample | Little-endian bytes |
| --- | ---: | --- |
| Full negative | `-4095` / `0xF001` as two's complement | `01 F0` |
| Zero | `0` / `0x0000` | `00 00` |
| Full positive | `4095` / `0x0FFF` | `FF 0F` |

Timing, offset, and period:

[IMPLEMENTED] `SET_WAVEFORM` does not carry an update-rate field. The host must compute offset and period sample counts for the same `UpdateRate` that will later be passed to `START`. The firmware interprets offset and period only as sample counts.

Use these relationships when constructing requests:

```text
sample_count = duration_seconds * update_rate_hz
duration_ms  = sample_count * 1000 / update_rate_hz
```

CommLib computes offset and period counts from milliseconds using `round(update_rate_hz * milliseconds / 1000)`.

[IMPLEMENTED] One waveform period consists of:

1. `offset` samples of zero output.
2. `n` signed waveform samples from the request.
3. If `period > offset + n`, trailing zero-output samples until `period` samples have elapsed.

[IMPLEMENTED] If the request period is `0`, the firmware sets `period = offset + n`, so there is no explicit trailing zero region. If the request period is non-zero and `offset + n > period`, the command returns `ECP_STIMULUS_PERIOD_TOO_SHORT_ERR`.

Repeat behavior:

[IMPLEMENTED] `waveRepeat` is loaded from the request header and controls how many periods are produced after the first period has started. Because the repeat counter is checked only when the first period completes, a non-empty waveform with repeat count `0` or `1` produces one period. A repeat count of `2` produces two periods, and so on.

[IMPLEMENTED] When the waveform engine reaches its final period, it outputs zero on both waveform DAC channels and marks the program inactive. The waveform completion path itself does not restore `defaultOutputVoltage`; after the main system loop observes that program activity has ended, `System_Stop(0)` calls `Generator_Stop`, which returns the analog output to `defaultOutputVoltage`.

Execution model:

[IMPLEMENTED] `Program_Start` activates the waveform only when the stored program type is `PRG_WAVEFORM` and the sample count is non-zero. It resets the waveform sample index to the first sample at byte offset 6 and starts at period position `pc = 0`.

[IMPLEMENTED] During each generator update, if the current period position is inside `[offset, offset + sample count)`, the firmware reads the next signed sample and advances the sample address. If the current position is before the offset or after the sample table but before the period end, it outputs zero. At the period boundary, it either starts another period or stops the waveform according to `waveRepeat`.

[IMPLEMENTED] Waveform generation can run at the same time as a trigger sequence. The final generator update combines the waveform DAC fields with the current trigger-sequence output fields.

Construction guidance:

- Use `SET_WAVEFORM` when the desired analog stimulus is easiest to express as one signed sample per generator update.
- Use `SET_STIMULUS_PROGRAM` instead when the desired stimulus is a compact sequence of absolute levels and ramps.
- Compute `offset`, `period`, and the intended sample duration using the same update rate later passed to `START`.
- Set `period = 0` when the period should be exactly `offset + sample count`.
- Set `period > offset + sample count` when a zero-output tail is needed before the waveform repeats or stops.
- Keep the payload length exactly `6 + 2 * sample_count` and keep sample count at or below `1000`.
- Treat the firmware limit of `1000` samples as authoritative. CommLib contains a `MaximumNumberOfInstructions` value of `1024` for `SetWaveform`, but the firmware rejects sample counts greater than `MAXIMAL_NUMBER_OF_SAMPLES` (`1000`).
- Use an extended ECP frame for waveforms whose payload length is `128` bytes or larger; this firmware interprets a second frame byte with its high bit set as an extended-frame control byte, not as a standard length.

Example: three-sample waveform, no offset, no trailing zero region, one period.

```text
repeat = 1         -> 01 00
offset = 0         -> 00 00
period = 0         -> 00 00  ; firmware uses offset + sample_count = 3
samples = [-4095, 0, +4095]
sample bytes = 01 F0 00 00 FF 0F
payload = 01 00 00 00 00 00 01 F0 00 00 FF 0F
```

Example: at `CLK1000Hz`, wait 10 ms, play 3 samples, then output zero until a 20 ms period completes, repeated twice.

```text
update_rate_hz = 1000
offset = 10 ms * 1000 Hz / 1000 = 10 = 0x000A
sample_count = 3
period = 20 ms * 1000 Hz / 1000 = 20 = 0x0014
repeat = 2
header bytes = 02 00 0A 00 14 00
```

On success, initializes `PRG_WAVEFORM` and returns ACK.

Implemented constraints:

- System state must be `STATE_IDLE`.
- Request length must be at least 6.
- Request length must be divisible by 2.
- Sample count must be at most `MAXIMAL_NUMBER_OF_SAMPLES` (`1000`).
- If period is non-zero, `offset + sample count` must not exceed period.

Possible handler errors:

- `ECP_ATTEMPT_TO_SET_WAVEFORM_WHILE_SYSTEM_IS_NOT_IDLE_ERR`
- `ECP_WAVEFORM_TOO_SHORT_ERR`
- `ECP_WAVEFORM_WRONG_SIZE_ERR`
- `ECP_WAVEFORM_TOO_LONG_ERR`
- `ECP_INVALID_STIMULUS_PROGRAM_TYPE_ERR`
- `ECP_STIMULUS_PERIOD_TOO_SHORT_ERR`

### `START` (`0x16`)

Request length: 8.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `TriggerSource` |
| 1 | `uint8` | `UpdateRate` |
| 2 | `uint8` | Reset program on completion, non-zero true |
| 3 | `uint8` | Restart on completion, non-zero true |
| 4 | `uint16` | Trigger sequence repeat count |
| 6 | `uint16` | Stimulus program repeat count |

Description:

[IMPLEMENTED] Starts or arms the generator using the previously loaded stimulus program and/or trigger sequence. The command is accepted only from `STATE_IDLE`. For `TRIG_NONE`, the firmware attempts to configure the generator timer immediately, starts the program and trigger sequence generators, marks `SOURCE_GENERATOR_START`, updates the first output sample, and enters `STATE_ACTIVE` if generation can run. For external trigger sources, the firmware stores the requested start configuration and enters `STATE_PENDING`; the actual `System_Start` call occurs later when the configured trigger input, button, or response-port trigger event is observed.

[IMPLEMENTED] `resetOnCompletion` causes `System_Stop` to reset loaded stimulus and trigger definitions after completion. `restartOnCompletion` is allowed only for externally triggered pending starts; when a non-forced stop occurs, the system re-enters pending state with the previous trigger source and repeat settings. `restartOnCompletion` is rejected for internally triggered (`TRIG_NONE`) starts.

On success, starts immediately for `TRIG_NONE` or enters pending state for external trigger sources, then returns ACK.

Implemented trigger handling:

- `TRIG_NONE`: starts internally immediately. `restartOnCompletion` is rejected.
- `TRIG_IN`, `TRIG_BUTTON`, `TRIG_TRIGGER_PORT01`, `TRIG_TRIGGER_PORT02`: stores pending start configuration.
- Other values return `ECP_INVALID_TRIGGER_ERR`.

Possible handler errors:

- `ECP_STARTING_GENERATOR_WHILE_NOT_IDLE_ERR`
- `ECP_INVALID_REQUEST_LENGTH_ERR`
- `ECP_CANNOT_RESTART_AN_INTERNALLY_TRIGGERED_PROGRAM_ERR`
- `ECP_INVALID_UPDATE_RATE_ERR`
- `ECP_GENERATOR_NOT_STARTED_ERR`
- `ECP_INVALID_TRIGGER_ERR`

### `SET_TRIGGER` (`0x17`)

Request length: 3.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Trigger output bitfield: bit 0 = trigger output, bit 1 = stimulus trigger output |
| 1 | `uint16` | Default trigger code |

Description:

[IMPLEMENTED] Updates the default trigger output state used when no trigger sequence entry is actively driving outputs. The low two bits of the bitfield control the trigger output and stimulus-trigger output, and the code field is written to the interface output port by `Generator_SetDefaultTrigger`. If the generator is currently active, the new default state is stored but not immediately forced onto the hardware outputs by this handler.

On success, updates the default trigger state and returns ACK. If the system is not active, the generator output is updated immediately.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `SET_VOLTAGE_OUT` (`0x18`)

Request length: 4.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint32` | Raw default output voltage code |

Description:

[IMPLEMENTED] Updates the raw default analog output value used before and after stimulus program execution. If the system is idle, the firmware immediately converts the raw value around `MIDPOINT` into the two DAC channels and writes it to the analog output. If the system is not idle, the value is stored and will be used when the generator stops or when a future program starts from the default value.

On success, stores the default output voltage and returns ACK. If the system is idle, the generator output voltage is updated immediately.

[INFERRED] CommLib encodes -10 V to +10 V into the full `uint32` range, with 0 V near the midpoint.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `CLEAR_PROGRAMS` (`0x19`)

Request length: 0.

Description:

[IMPLEMENTED] Forces any active or pending operation toward an idle, no-program state. If the system is not idle, the handler calls `System_Stop(1)` as a forced stop, which disables generator activity and prevents automatic restart from `restartProgramOnCompletion`. It then calls `Program_Reset`, clearing both the stimulus program type and trigger sequence type.

On success, stops the system when not idle, resets stimulus and trigger programs, and returns ACK.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `STOP` (`0x20`)

Request length: 1.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Reset programs, non-zero true |

Description:

[IMPLEMENTED] Stops current operation without necessarily clearing the loaded program definitions. If the system is active, `System_Stop(1)` disables the generator timer, returns analog output and trigger outputs to their default states, and sets the system state to idle. Because the stop is forced, automatic restart-on-completion behavior is not applied. If the request reset byte is non-zero, the firmware also clears both the stimulus and trigger program definitions.

On success, stops the system when not idle, optionally resets stimulus and trigger programs, and returns ACK.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `SET_REQUIRED_DEVICES` (`0x21`)

Request length: 4.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Required `ResponseDevice` for port 01 |
| 1 | `uint8` | Required `DeviceSubclass` for port 01 |
| 2 | `uint8` | Required `ResponseDevice` for port 02 |
| 3 | `uint8` | Required `DeviceSubclass` for port 02 |

Description:

[IMPLEMENTED] Stores the required response-device type and subclass for both response ports. The command itself only updates `system.requiredDevices`; it does not immediately validate the connected devices. Validation happens during the system update loop, where a mismatch sets `system.errorCode` to `INCORRECT_RESPONSE_DEVICE` and moves the system to `STATE_ERROR`. A required device value of `DEVICE_NONE` disables the type requirement for that port, and a required subclass of `DEVICE_SUBCLASS_NONE` disables subclass matching for a non-none required device.

On success, updates the required response-device configuration and returns ACK.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `SET_TIMING_SOURCE` (`0x22`)

Request length: 2.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint8` | `TimingSource` |

Description:

[IMPLEMENTED] Selects which timing mark a connected response device should use for its measurements on the selected response port. The response layer validates the port and then stores the selected `TimingSource` in the corresponding `Device` structure. The operation does not require a particular connected device type in the analyzed `Response_SetTimingSource` implementation.

On success, returns ACK.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`. Response-device failures are mapped through `ResponseStatus`.

### `SET_TRIGGER_ARMING_PERIOD` (`0x23`)

Request length: 3.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint16` | Arming period |

Description:

[IMPLEMENTED] Configures the arming period for a response device on the selected port. The response layer accepts this operation for trigger devices and sensor devices, dispatching to the corresponding device driver. Other connected device types return a wrong-device error. The period value is passed through as a raw `uint16`; any device-specific range validation is performed below the peripheral handler.

On success, returns ACK.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`. Response-device failures are mapped through `ResponseStatus`.

### `SET_SIGNAL_SAMPLE_PERIOD` (`0x24`)

Request length: 3.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint16` | Sample period |

Description:

[IMPLEMENTED] Configures how often a scale or sensor response device samples and reports signal data. The response layer first validates the response port, then rejects periods below `50` or above `1000`, and finally dispatches to the scale or sensor device driver. Trigger devices, button devices, and other unsupported response-device types return a wrong-device error.

On success, returns ACK.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`. Response-device failures are mapped through `ResponseStatus`.

### `GET_ANALOG_VALUE` (`0x25`)

Request length: 1.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `AnalogChannel` |

Response length: 2.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint16` | ADC sample value |

Description:

[IMPLEMENTED] Reads one firmware ADC channel and returns the most recent `ADC_GetValue` result as a raw `uint16`. The request byte is cast to the firmware analog channel type and passed directly to the ADC layer. The handler does not perform range validation beyond checking the one-byte request length.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `SET_TRIGGER_LEVEL` (`0x32`)

Request length: 3.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint16` | Trigger level |

Description:

[IMPLEMENTED] Sets the analog threshold level for a sensor device on the selected response port. The response layer validates the port and accepts this operation only when the detected response device is `DEVICE_SENSOR`; other response-device types return a wrong-device error. The level is passed through as a raw `uint16` to `SensorDevice_SetTriggerLevel`.

On success, returns ACK.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`. Response-device failures are mapped through `ResponseStatus`.

### `WRITE_SERIAL_NUMBER` (`0x40`)

Expected request length: 2.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint16` | Serial number |

Description:

[IMPLEMENTED] Writes a new serial number record to EEPROM at `SERIAL_NUMBER_ADDR`. The handler creates a local serial record, copies the request `uint16` into it, sets its valid flag to `1`, saves it through `SerialNumber_Save`, and acknowledges the request. The in-memory `system.serialNumber` value is not explicitly reloaded by this handler; the new value is read into system state during normal initialization after a reset or power cycle.

On success, writes the serial number with `valid = 1` and returns ACK.

[IMPLEMENTED] This handler does not validate request length before reading the serial number.

### `WRITE_CALIBRATION` (`0x41`)

Request length: 13.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `CalibratorID` |
| 1 | `uint8` | Calibration record valid marker |
| 2 | `int32` | Calibration coefficient `a`, fixed-point Q12 in CommLib |
| 6 | `int32` | Calibration coefficient `b`, fixed-point Q12 in CommLib |
| 10 | `uint16` | Maximum value |
| 12 | `uint8` | Calibration checksum |

Description:

[IMPLEMENTED] Writes one response-port calibration record to EEPROM and refreshes calibration in the response subsystem. The calibrator ID selects the EEPROM address for response port 01 or 02. The handler builds a `Calibrator` object from the request fields, and `Calibrator_Save` writes it only if the valid marker and checksum are accepted by the calibration serializer/checker. After a successful save, `Response_ReloadCalibration` reloads calibration into all response-device objects.

On success, saves the calibration record, reloads response calibration, and returns ACK.

Possible handler errors:

- `ECP_INVALID_REQUEST_LENGTH_ERR`
- `ECP_INVALID_CALIBRATION_ADDRESS_ERR`
- `ECP_COULD_NOT_SAVE_TO_EEPROM_ERR`

### `READ_CALIBRATION` (`0x42`)

Expected request length: 1.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `CalibratorID` |

Response length: 12.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Calibration record valid marker |
| 1 | `int32` | Calibration coefficient `a` |
| 5 | `int32` | Calibration coefficient `b` |
| 9 | `uint16` | Maximum value |
| 11 | `uint8` | Calibration checksum |

Description:

[IMPLEMENTED] Reads one response-port calibration record from EEPROM. The handler initializes a calibrator object with defaults for the requested ID, then calls `Calibrator_Load`; if the EEPROM block is valid and has a matching checksum, the stored values replace the defaults, otherwise the initialized defaults remain. The response payload therefore contains either the stored valid calibration or the default initialized calibration values.

Possible handler error:

- `ECP_INVALID_CALIBRATION_ADDRESS_ERR`

[IMPLEMENTED] This handler does not validate request length before reading the calibrator ID.

### `GET_EVENT` (`0x46`)

Request length: 1.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `EventType` |

Response length: 73.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Valid flag |
| 1 | `uint32` | Event ID |
| 5 | `uint16` | Year |
| 7 | `uint8` | Month |
| 8 | `uint8` | Day |
| 9 | `uint8[64]` | Event text |

Description:

[IMPLEMENTED] Reads a build or calibration event record from EEPROM. The event type selects the EEPROM address. If the stored record starts with the valid marker, the firmware returns the stored ID, date, and text with `valid = 1`; otherwise it returns `valid = 0`, ID `0`, date `9999-12-31`, and an empty text prefix.

Possible handler errors:

- `ECP_INVALID_REQUEST_LENGTH_ERR`
- `ECP_INVALID_EVENT_ADDRESS_ERR`

### `SET_EVENT` (`0x47`)

Request length: 74.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `EventType` |
| 1 | `uint8` | Valid flag |
| 2 | `uint32` | Event ID |
| 6 | `uint16` | Year |
| 8 | `uint8` | Month |
| 9 | `uint8` | Day |
| 10 | `uint8[64]` | Event text |

Description:

[IMPLEMENTED] Writes a build or calibration event record to EEPROM. The event type selects the EEPROM address. If the request valid flag is non-zero, the firmware writes the valid marker, ID, date, and 64 text bytes. If the request valid flag is zero, the firmware invalidates the record by writing `0xFF` to the record's first byte and does not rewrite the remaining record fields.

On success, saves the event record and returns ACK.

Possible handler errors:

- `ECP_INVALID_REQUEST_LENGTH_ERR`
- `ECP_INVALID_EVENT_ADDRESS_ERR`

### `RESET` (`0x48`)

Request length: 0.

Description:

[IMPLEMENTED] Acknowledges the command, flushes pending serial output, and then enters an infinite loop. The code relies on the platform's reset/watchdog behavior outside this handler to recover from that loop. The handler does not clear programs, EEPROM records, or runtime state before entering the loop.

On success, sends ACK, flushes the serial port, and then waits forever.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `SET_INTERFACE_LOGIC` (`0x49`)

Request length: 3.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Expected low-byte `VoltageLevel` |
| 1 | `uint8` | Expected high-byte `VoltageLevel` |
| 2 | `uint8` | `Logic` |

Description:

[IMPLEMENTED] Configures the expected voltage levels and active logic convention for the external interface port. The firmware acknowledges the request before applying the new settings, then stores the expected low-byte and high-byte voltage levels in `system` and calls `DIO_SetLogic`. The configured expected voltage levels are later checked by `System_CheckInterfacePort`; mismatches set `INCORRECT_INTERFACE_VOLTAGE_LEVELS` and can move the system into `STATE_ERROR`.

On success, sends ACK, then updates interface voltage-level expectations and interface logic.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

### `GET_INTERFACE_STATUS` (`0x50`)

Request length: 0.

Response length: 4.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Current low-byte `VoltageLevel` |
| 1 | `uint8` | Current high-byte `VoltageLevel` |
| 2 | `uint8` | Interface voltage configuration valid, non-zero true |
| 3 | `uint8` | Current `Logic` |

Description:

[IMPLEMENTED] Reports the measured voltage levels of the low and high halves of the external interface port, whether those measurements match the expected levels currently stored in `system`, and the active logic convention. The validity byte is computed by `System_CheckInterfacePort`; as a side effect, an invalid result updates `system.errorCode` to `INCORRECT_INTERFACE_VOLTAGE_LEVELS`.

Invalid request length returns `ECP_INVALID_REQUEST_LENGTH_ERR`.

## Messages

### Summary

| Code | Name | Length | Emitted by analyzed code |
| ---: | --- | ---: | --- |
| `0x80` | `SYSTEM_STATE_UPDATE` | 7 | Yes |
| `0x81` | `EVENT_UPDATE` | 1 | Yes |
| `0x90` | `SIGNAL_MSG` | 21 | Yes |
| `0x91` | `BUTTON_MSG` | 10 | Yes |
| `0x92` | `DEVICE_CHANGED_MSG` | Unknown | Defined, not emitted |
| `0x93` | `TRIGGER_MSG` | 9 | Yes |
| `0x94` | `ANALOG_INPUT_MSG` | 13 in CommLib | Defined, not emitted |
| `0x95` | `THRESHOLD_MSG` | 19 | Yes |
| `0xFF` | `PRINTF_MSG` | Variable | Yes |

### `SYSTEM_STATE_UPDATE` (`0x80`)

[IMPLEMENTED] Sent periodically every `STATUS_UPDATE_PERIOD` (`100`) timer units by `PeripheralHandler_OnStatusTimer`.

Payload length: 7.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `State` |
| 1 | `uint8` | Port 01 `ResponseDevice` |
| 2 | `uint8` | Port 01 `DeviceSubclass` |
| 3 | `uint8` | Port 02 `ResponseDevice` |
| 4 | `uint8` | Port 02 `DeviceSubclass` |
| 5 | `uint8` | Power-on flag |
| 6 | `uint8` | `SystemError` |

### `EVENT_UPDATE` (`0x81`)

[IMPLEMENTED] Sent when queued system events are processed.

Payload length: 1.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `EventID` |

### `SIGNAL_MSG` (`0x90`)

[IMPLEMENTED] Sent by `System_OnSignal`.

Payload length: 21.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint8` | `ResponseDevice` |
| 2 | `uint8` | `DeviceSubclass` |
| 3 | `uint16` | Signal |
| 5 | `int32` | Calibration coefficient `a`, fixed-point Q12 in CommLib |
| 9 | `int32` | Calibration coefficient `b`, fixed-point Q12 in CommLib |
| 13 | `uint16` | Maximum value |
| 15 | `int16` | Target |
| 17 | `int16` | High limit |
| 19 | `int16` | Low limit |

### `BUTTON_MSG` (`0x91`)

[IMPLEMENTED] Sent by `System_OnButton`.

Payload length: 10.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint8` | `ResponseDevice` |
| 2 | `uint8` | `DeviceSubclass` |
| 3 | `uint8` | Button identifier |
| 4 | `uint8` | Button state |
| 5 | `uint8` | Timer ticks per millisecond |
| 6 | `uint32` | Button time in timer ticks |

### `DEVICE_CHANGED_MSG` (`0x92`)

[IMPLEMENTED] The code is defined in `SystemConfig.h`.

[UNKNOWN] No analyzed firmware code emits this message. `System_OnResponseChanged` updates `system.devices` but does not transmit `DEVICE_CHANGED_MSG`.

### `TRIGGER_MSG` (`0x93`)

[IMPLEMENTED] Sent by `System_OnTrigger`.

Payload length: 9.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint8` | `ResponseDevice` |
| 2 | `uint8` | `DeviceSubclass` |
| 3 | `uint8` | Trigger code |
| 4 | `uint8` | Timer ticks per millisecond |
| 5 | `uint32` | Trigger time in timer ticks |

### `ANALOG_INPUT_MSG` (`0x94`)

[IMPLEMENTED] The code is defined in `SystemConfig.h`, and CommLib defines a 13-byte message layout.

[UNKNOWN] No analyzed firmware code emits this message.

CommLib layout:

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | Pin |
| 1 | `uint16` | Signal |
| 3 | `int32` | Calibration coefficient `a`, fixed-point Q12 in CommLib |
| 7 | `int32` | Calibration coefficient `b`, fixed-point Q12 in CommLib |
| 11 | `uint16` | Maximum value |

### `THRESHOLD_MSG` (`0x95`)

[IMPLEMENTED] Sent by `System_OnThreshold`.

Payload length: 19.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8` | `ResponsePort` |
| 1 | `uint8` | `ResponseDevice` |
| 2 | `uint8` | `DeviceSubclass` |
| 3 | `uint16` | Signal |
| 5 | `int32` | Calibration coefficient `a`, fixed-point Q12 in CommLib |
| 9 | `int32` | Calibration coefficient `b`, fixed-point Q12 in CommLib |
| 13 | `uint16` | Maximum value |
| 15 | `uint32` | Response time |

### `PRINTF_MSG` (`0xFF`)

[IMPLEMENTED] Sent by `PeripheralHandler_Printf`.

Payload length: variable string length.

| Offset | Type | Meaning |
| ---: | --- | --- |
| 0 | `uint8[length]` | String bytes from the supplied C string, without an added null terminator |

## Enumerations

### `EcpError`

| Value | Name |
| ---: | --- |
| 0 | `ECP_NO_ERROR` |
| 1 | `ECP_UNKNOWN_FUNCTION_ERR` |
| 2 | `ECP_CHECKSUM_ERR` |
| 3 | `ECP_INVALID_REQUEST_LENGTH_ERR` |
| 4 | `ECP_INVALID_NUMBER_OF_DEBUG_SIGNALS_ERR` |
| 5 | `ECP_ATTEMPT_TO_SET_PROGRAM_WHILE_SYSTEM_IS_NOT_IDLE_ERR` |
| 6 | `ECP_INVALID_LENGTH_OF_STIMULUS_PROGRAM_ERR` |
| 7 | `ECP_STIMULUS_PROGRAM_IS_TOO_LONG_ERR` |
| 8 | `ECP_ATTEMPT_TO_SET_TRIGGER_SEQUENCE_WHILE_SYSTEM_IS_NOT_IDLE_ERR` |
| 9 | `ECP_ATTEMPT_TO_SET_WAVEFORM_WHILE_SYSTEM_IS_NOT_IDLE_ERR` |
| 10 | `ECP_WAVEFORM_TOO_SHORT_ERR` |
| 11 | `ECP_WAVEFORM_WRONG_SIZE_ERR` |
| 12 | `ECP_WAVEFORM_TOO_LONG_ERR` |
| 13 | `ECP_WAVEFORM_REPEATED_ZERO_TIMES_ERR` |
| 14 | `ECP_STARTING_GENERATOR_WHILE_NOT_IDLE_ERR` |
| 15 | `ECP_GENERATOR_NOT_STARTED_ERR` |
| 16 | `ECP_INVALID_TRIGGER_ERR` |
| 17 | `ECP_CANNOT_SET_VOLTAGE_AS_PROGRAM_IS_ACTIVE_ERR` |
| 18 | `ECP_NO_SUITABLE_RESPONSE_DEVICE_CONNECTED_ERR` |
| 19 | `ECP_TRIGGER_SYSTEM_NOT_MANUAL_MODE_ERR` |
| 20 | `ECP_INVALID_LENGTH_OF_TRIGGER_SEQUENCE_ERR` |
| 21 | `ECP_TRIGGER_SEQUENCE_TOO_LONG_ERR` |
| 22 | `ECP_INVALID_UPDATE_RATE_ERR` |
| 23 | `ECP_INVALID_EVENT_ADDRESS_ERR` |
| 24 | `ECP_INVALID_STIMULUS_PROGRAM_TYPE_ERR` |
| 25 | `ECP_STIMULUS_PERIOD_TOO_SHORT_ERR` |
| 26 | `ECP_CANNOT_SET_BUILD_EVENT_ERR` |
| 27 | `ECP_COULD_NOT_SAVE_TO_EEPROM_ERR` |
| 28 | `ECP_INVALID_CALIBRATION_ADDRESS_ERR` |
| 29 | `ECP_CANNOT_RESTART_AN_INTERNALLY_TRIGGERED_PROGRAM_ERR` |
| 30 | `ECP_INVALID_PORT_ERR` |
| 31 | `ECP_I2C_WRITE_FAILED_ERR` |
| 32 | `ECP_I2C_READ_FAILED_ERR` |
| 33 | `ECP_DATA_VERIFY_FAILED_ERR` |
| 34 | `ECP_SAMPLE_PERIOD_TOO_LOW_ERR` |
| 35 | `ECP_SAMPLE_PERIOD_TOO_HIGH_ERR` |
| 36 | `ECP_INVALID_PARAMTER_ERR` |
| 37 | `ECP_INVALID_STATE_ERR` |
| 38 | `ECP_NO_PROGRAM_ERR` |

### Response Status Error Mapping

[IMPLEMENTED] Response-device functions map `ResponseStatus` to ECP ACK/NAK as follows.

| `ResponseStatus` | ECP result |
| --- | --- |
| `RESPONSE_STATUS_SUCCESS` | ACK |
| `RESPONSE_STATUS_WRONG_DEVICE_TYPE` | `ECP_NO_SUITABLE_RESPONSE_DEVICE_CONNECTED_ERR` |
| `RESPONSE_STATUS_INVALID_PORT` | `ECP_INVALID_PORT_ERR` |
| `RESPONSE_STATUS_I2C_WRITE_FAILED` | `ECP_I2C_WRITE_FAILED_ERR` |
| `RESPONSE_STATUS_I2C_READ_FAILED` | `ECP_I2C_READ_FAILED_ERR` |
| `RESPONSE_STATUS_DATA_VERIFY_FAILED` | `ECP_DATA_VERIFY_FAILED_ERR` |
| `RESPONSE_STATUS_SAMPLE_PERIOD_TOO_LOW` | `ECP_SAMPLE_PERIOD_TOO_LOW_ERR` |
| `RESPONSE_STATUS_SAMPLE_PERIOD_TOO_HIGH` | `ECP_SAMPLE_PERIOD_TOO_HIGH_ERR` |
| `RESPONSE_STATUS_INVALID_PARAMTER` | `ECP_INVALID_PARAMTER_ERR` |
| `RESPONSE_STATUS_INVALID_STATE` | `ECP_INVALID_STATE_ERR` |
| `RESPONSE_STATUS_NO_PROGRAM` | `ECP_NO_PROGRAM_ERR` |
| Any other value | `ECP_NO_SUITABLE_RESPONSE_DEVICE_CONNECTED_ERR` |

### Common Field Enumerations

| Type | Values |
| --- | --- |
| `State` | `0` = `STATE_IDLE`, `1` = `STATE_PENDING`, `2` = `STATE_ACTIVE`, `3` = `STATE_ERROR` |
| `SystemError` | `0` = `NO_ERROR`, `1` = `NO_POWER_ERROR`, `2` = `INCORRECT_RESPONSE_DEVICE`, `3` = `INCORRECT_INTERFACE_VOLTAGE_LEVELS` |
| `ResponsePort` | `0` = `RESPONSE_PORT01`, `1` = `RESPONSE_PORT02` |
| `ResponseDevice` | `0` = `DEVICE_NONE`, `1` = `DEVICE_SCALE`, `2` = `DEVICE_DIGITAL`, `3` = `DEVICE_BUTTON`, `4` = `DEVICE_RESERVED01`, `5` = `DEVICE_SENSOR`, `6` = `DEVICE_TRIGGER`, `7` = `DEVICE_RESPONSE_INPUT`, `8` = `DEVICE_RESERVED02`, `9` = `DEVICE_RESERVED03` |
| `DeviceSubclass` | `0` = `DEVICE_SUBCLASS_NONE`, `1` through `9` = `DEVICE_SUBCLASS01` through `DEVICE_SUBCLASS09` |
| `TriggerSource` | `0` = `TRIG_NONE`, `1` = `TRIG_IN`, `2` = `TRIG_BUTTON`, `3` = `TRIG_TRIGGER_PORT01`, `4` = `TRIG_TRIGGER_PORT02` |
| `UpdateRate` | `0` = 125 Hz, `1` = 250 Hz, `2` = 500 Hz, `3` = 1000 Hz, `4` = 2000 Hz, `5` = 5000 Hz, `6` = 10000 Hz, `7` = 20000 Hz |
| `TimingSource` | `0` = `SOURCE_TRIG_IN`, `1` = `SOURCE_GENERATOR_START`, `2` = `SOURCE_PORT01`, `3` = `SOURCE_PORT02`, `4` = `SOURCE_EOL` |
| `VoltageLevel` | `0` = `VOLTAGE_LEVEL_UNCONNECTED`, `1` = `VOLTAGE_LEVEL_V3P3`, `2` = `VOLTAGE_LEVEL_V5P0`, `3` = `VOLTAGE_LEVEL_INVALID` |
| `Logic` | `0` = `LOGIC_POSITIVE`, `1` = `LOGIC_NEGATIVE` |
| `CalibratorID` | `0` = `ID_RSP01_CALIBRATOR`, `1` = `ID_RSP02_CALIBRATOR` |
| `EventType` | `0` = `BUILD_EVENT`, `1` = `CALIBRATION_EVENT` |
| `Opcode` | `0x00` = `NOP`, `0x02` = `INC`, `0x04` = `DEC`, `0x06` = `SET` |

### `AnalogChannel`

| Value | Name |
| ---: | --- |
| 0 | `RES1_RATING` |
| 1 | `RES2_RATING` |
| 2 | `RES1_DETECT` |
| 3 | `RES2_DETECT` |
| 4 | `RES1_DDF06` |
| 5 | `RES2_DDF06` |
| 6 | `TRIG_S13` |
| 7 | `TRIG_S25` |
| 8 | `TRIG_MISC` |
| 9 | `TRIG_VTL` |
| 10 | `TRIG_VTH` |
| 11 | `SUPPLY_VOLTAGE` |

### `EventID`

| Value | Name |
| ---: | --- |
| 0 | `EVT_NO_EVENT` |
| 1 | `EVT_BUTTON_PRESSED` |
| 2 | `EVT_12V_POWER_ON` |
| 3 | `EVT_12V_POWER_OFF` |
| 4 | `EVT_TRIG_IN_ACTIVE` |
| 5 | `EVT_PROGRAM_COMPLETE` |
| 6 | `EVT_PROGRAM_TIMEOUT` |
| 7 | `EVT_TRIGGER_TIMEOUT` |
| 8 | `EVT_TRIGGER_PORT01` |
| 9 | `EVT_TRIGGER_PORT02` |
| 10 | `EVT_THRESHOLD_PORT01` |
| 11 | `EVT_THRESHOLD_PORT02` |

## Implementation Notes and Gaps

[IMPLEMENTED] The packet receive buffer for ordinary request data is `MAX_PACKET_SIZE` (`128`) bytes, but `SET_STIMULUS_PROGRAM`, `SET_WAVEFORM`, and `SET_TRIGGER_SEQUENCE` use dedicated larger program or trigger buffers.

[IMPLEMENTED] The firmware uses the request code to select the backing memory before the full packet has been received.

[IMPLEMENTED] `WRITE_SERIAL_NUMBER` and `READ_CALIBRATION` read request fields without validating request length. Their expected request lengths are documented from the accessed fields and CommLib definitions.

[IMPLEMENTED] `DEVICE_CHANGED_MSG` and `ANALOG_INPUT_MSG` are defined message codes, but no analyzed firmware path emits them.
