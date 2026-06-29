## Issue Metadata

- **ID:** `T0001`
- **Title:** `Align LIO status and response-device enums with the IDD`
- **Status:** `Review`
- **Type:** `Bug`
- **Related Work:** `.documentation/documentation/lio/interface-design-description.md`

## Summary

Correct the public LIO enum values and status-message decoding so they match the LabBench I/O IDD byte values directly. Preserve practical compatibility aliases only when they do not hide the IDD-canonical names and values.

## Problem Statement

- **Current behavior:** `src/labbench_comm/devices/lio/definitions.py` defines `DeviceState.STATE_NOT_CONNECTED = 0`, then shifts `STATE_IDLE` through `STATE_ERROR` to values `1..4`. `StatusMessage.state` compensates by returning `DeviceState(self.packet.get_byte(0) + 1)`. The same file names response-device value `4` as `DEVICE_RESPONSE` and misspells value `7` as `DEVICE_REPONSE_INPUT`, while the IDD names them `DEVICE_RESERVED01` and `DEVICE_RESPONSE_INPUT`.
- **Desired behavior:** The enum members exposed by `labbench_comm.devices.lio` use the IDD values directly: `STATE_IDLE = 0`, `STATE_PENDING = 1`, `STATE_ACTIVE = 2`, `STATE_ERROR = 3`; response-device values include `DEVICE_RESERVED01 = 4` and `DEVICE_RESPONSE_INPUT = 7`. `StatusMessage.state` decodes the firmware byte without an offset.
- **Why this matters:** LIO status bytes and public enum values are part of the host-device contract. Shifted or misnamed enum values can cause incorrect comparisons, user code that serializes enum values incorrectly, and confusion when debugging against firmware traces.

## Scope

### In Scope

- Update `DeviceState` and `ResponseDevice` in `src/labbench_comm/devices/lio/definitions.py` to align with the IDD.
- Update `StatusMessage.state` in `src/labbench_comm/devices/lio/messages/status_message.py` to decode byte `0` directly.
- Update `LIOCentral` initialization in `src/labbench_comm/devices/lio/lio_central.py` if it currently depends on `STATE_NOT_CONNECTED`.
- Update LIO tests and examples that use the non-IDD response-device names.
- Keep backwards-compatible aliases for `DEVICE_RESPONSE = 4` and `DEVICE_REPONSE_INPUT = 7` only if doing so does not make the non-IDD names canonical in iteration or docs. Prefer defining IDD names first and aliases after them if aliases are retained.

### Out of Scope

- Renaming unrelated function classes whose packet codes and layouts already match the IDD.
- Implementing missing LIO functions; that is covered by `T0002`.
- Changing CPAR+ enums or status decoding.

## Context for Implementation Agent

- **Relevant files and directories:**
  - `src/labbench_comm/devices/lio/definitions.py`: contains the enum definitions to correct.
  - `src/labbench_comm/devices/lio/messages/status_message.py`: currently adds `+ 1` when decoding `DeviceState`.
  - `src/labbench_comm/devices/lio/lio_central.py`: initializes `self.state = DeviceState.STATE_NOT_CONNECTED`.
  - `tests/devices/lio/test_lio_central.py`: currently asserts the misspelled `ResponseDevice.DEVICE_REPONSE_INPUT` and status decoding through the shifted enum.
  - `examples/lio/monitor_response_ports.py`: currently uses `ResponseDevice.DEVICE_RESPONSE`.
- **External or internal references:**
  - `.documentation/documentation/lio/interface-design-description.md`, section `Common Field Enumerations`: `State` values are `0 = STATE_IDLE`, `1 = STATE_PENDING`, `2 = STATE_ACTIVE`, `3 = STATE_ERROR`; `ResponseDevice` values are `0 = DEVICE_NONE`, `1 = DEVICE_SCALE`, `2 = DEVICE_DIGITAL`, `3 = DEVICE_BUTTON`, `4 = DEVICE_RESERVED01`, `5 = DEVICE_SENSOR`, `6 = DEVICE_TRIGGER`, `7 = DEVICE_RESPONSE_INPUT`, `8 = DEVICE_RESERVED02`, `9 = DEVICE_RESERVED03`.
  - `.documentation/documentation/lio/interface-design-description.md`, section `SYSTEM_STATE_UPDATE`: status payload offset `0` is the raw `State` byte.
- **Inputs, outputs, and contracts:**
  - A status packet with payload byte `0` equal to `0` must decode as `DeviceState.STATE_IDLE`.
  - A status packet with payload byte `0` equal to `3` must decode as `DeviceState.STATE_ERROR`.
  - Public enum numeric values must match the IDD exactly.
- **Known constraints:**
  - This package is typed and public; avoid unnecessary API breakage, but do not keep incorrect canonical names ahead of IDD names.
  - The IDD is the source of truth for LIO field names and values.
- **Risks and edge cases:**
  - Removing `STATE_NOT_CONNECTED` may require using `None` or an optional state for the initial not-yet-connected central state.
  - Keeping enum aliases can make the first-defined name canonical. Define the IDD name first when preserving aliases.

## Acceptance Criteria

- [x] `DeviceState.STATE_IDLE == 0`, `STATE_PENDING == 1`, `STATE_ACTIVE == 2`, and `STATE_ERROR == 3`.
- [x] `StatusMessage(Packet(0x80, 7) with byte 0 set to 0).state is DeviceState.STATE_IDLE` without adding an offset.
- [x] `StatusMessage(Packet(0x80, 7) with byte 0 set to 3).state is DeviceState.STATE_ERROR`.
- [x] `ResponseDevice.DEVICE_RESERVED01 == 4` and `ResponseDevice.DEVICE_RESPONSE_INPUT == 7` are available from `labbench_comm.devices.lio`.
- [x] Existing LIO state and callback behavior still works after receiving a status message.
- [x] Tests no longer require `ResponseDevice.DEVICE_REPONSE_INPUT` as the canonical IDD name.

## Definition of Done

- [x] All acceptance criteria pass.
- [x] The implementation follows existing repository patterns and keeps the change scoped to this issue.
- [x] Automated tests are added or updated for changed behavior, or a clear reason is documented for why tests are not appropriate.
- [x] Relevant manual validation is completed and documented in this issue.
- [x] Build, lint, type-check, formatting, and test commands relevant to the touched code pass.
- [x] User-facing text, docs, configuration, examples, or migration notes are updated when behavior changes.
- [x] Security, privacy, accessibility, performance, and compatibility implications were considered for the changed surface.
- [x] No unrelated files, generated artifacts, or user changes are reverted or modified.
- [x] Any follow-up work is explicitly listed with rationale.

## Implementation Notes

- **Suggested approach:** Update enum definitions first, then update `StatusMessage.state`, then update `LIOCentral` initial state and tests.
- **Preferred patterns/APIs:** Keep using `IntEnum` and existing `Packet` helpers.
- **Files likely to change:** `src/labbench_comm/devices/lio/definitions.py`, `src/labbench_comm/devices/lio/messages/status_message.py`, `src/labbench_comm/devices/lio/lio_central.py`, `tests/devices/lio/test_lio_central.py`, and possibly `examples/lio/monitor_response_ports.py`.
- **Files likely not to change:** CPAR+ device files and protocol packet framing code.
- **Migration/rollout notes:** If aliases are retained, note them in tests as compatibility aliases, not IDD-canonical names.
- **Testing notes:** Add explicit assertions for all four `DeviceState` numeric values and the two corrected `ResponseDevice` names.
- **Potential blockers:** None.

## Validation Plan

- **Automated checks:**
  - `pytest -m unittest tests/devices/lio/test_lio_central.py`: validates LIO enum values, status decoding, and LIO central callback behavior.
  - `pytest -m unittest`: validates the broader unit suite still passes.
- **Manual checks:**
  - Inspect `src/labbench_comm/devices/lio/definitions.py` and confirm the IDD-canonical names are the primary enum members.
- **Regression checks:**
  - Confirm `LIOCentral.on_status_message` still updates `state`, response ports, power, and error fields from a valid status packet.

## Implementation Agent Notes

- Status moved to `Review` after implementation and validation.
- Validation results:
  - `pytest -m unittest tests/devices/lio/test_lio_central.py` initially failed as expected after adding enum-value assertions: `DeviceState.STATE_IDLE` was still `1`.
  - `pytest -m unittest tests/devices/lio/test_lio_central.py`: passed, `27 passed`, with one pytest cache warning.
  - `python -m pytest -m unittest -v`: passed, `72 passed, 2 deselected`, with one pytest cache warning.
  - `python -m build`: first failed in the sandbox because isolated build dependency installation could not reach PyPI; reran with approved escalation and passed, building `labbench_comm-0.1.2.tar.gz` and `labbench_comm-0.1.2-py3-none-any.whl`.
- Manual checks:
  - Inspected `src/labbench_comm/devices/lio/definitions.py`; IDD names are defined before compatibility aliases, so `ResponseDevice(4).name` is `DEVICE_RESERVED01` and `ResponseDevice(7).name` is `DEVICE_RESPONSE_INPUT`.
  - No configured lint, type-check, or formatting commands were found in `pyproject.toml`, README, or CI.
- Follow-ups: None.
