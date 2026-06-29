## Issue Metadata

- **ID:** `T0002`
- **Title:** `Align the LIO function surface with implemented IDD functions`
- **Status:** `Review`
- **Type:** `Feature`
- **Related Work:** `.documentation/documentation/lio/interface-design-description.md`, `T0001`

## Summary

Add the LIO function classes that the IDD documents but the Python LIO package does not expose, and remove the stale non-IDD reset-calibration function from the public LIO surface. This closes host API gaps for `GET_ENDIANNESS`, `SET_INDICATORS`, and `WRITE_CALIBRATION`.

## Problem Statement

- **Current behavior:** The IDD lists implemented LIO function codes `0x03` (`GET_ENDIANNESS`), `0x12` (`SET_INDICATORS`), and `0x41` (`WRITE_CALIBRATION`), but `src/labbench_comm/devices/lio/functions/` has no corresponding classes or exports. The package exposes `ResetCalibration` with code `0x43`, but the IDD function summary does not list `0x43` as an implemented LIO function.
- **Desired behavior:** The LIO package exposes IDD-backed function classes for `GET_ENDIANNESS`, `SET_INDICATORS`, and `WRITE_CALIBRATION` with correct packet codes, request lengths, response lengths, and field accessors. The stale `ResetCalibration` function is removed from the public LIO API unless a newer local IDD entry is found before implementation.
- **Why this matters:** Users cannot call all implemented firmware functions through the library, while one exposed function appears unsupported by the source-of-truth IDD.

## Scope

### In Scope

- Add a `GetEndianness` LIO function class for code `0x03`, request length `0`, response length `2`, with an `endian_marker` or similarly clear property reading `response.get_uint16(0)`.
- Add a `SetIndicators` LIO function class for code `0x12`, request length `6`, response length `0`, with `port`, `led_bitfield`, and `duration` accessors mapped to offsets `0`, `1`, and `2`.
- Add a `WriteCalibration` LIO function class for code `0x41`, request length `13`, response length `0`, with accessors for `calibrator`, raw `valid_marker`, fixed-point/raw coefficients `a`/`ab` and `b`/`bb`, `maximum`, and `checksum`.
- Export the new classes from `src/labbench_comm/devices/lio/functions/__init__.py` and `src/labbench_comm/devices/lio/__init__.py`.
- Remove `ResetCalibration` from public exports and tests because it is not in the IDD. Delete the file only if no internal references remain and the removal is clean.
- Add or update unit tests for static packet shapes, field offsets, and exports.

### Out of Scope

- Running hardware integration tests or writing to real EEPROM.
- Implementing firmware behavior or changing the IDD.
- Renaming already working function classes such as `GetAnalogSignal` or `SetVoltage` solely to match IDD display names.
- Changing packet framing or checksum behavior.

## Context for Implementation Agent

- **Relevant files and directories:**
  - `src/labbench_comm/devices/lio/functions/`: location for LIO function classes.
  - `src/labbench_comm/devices/lio/functions/base.py`: defines `_LIOFunction`, `CALIBRATION_RECORD_SIZE`, `CALIBRATION_Q`, and `CALIBRATION_VALID_MARKER`.
  - `src/labbench_comm/devices/lio/functions/read_calibration.py`: existing read-side calibration layout and fixed-point access pattern.
  - `src/labbench_comm/devices/lio/functions/set_signal_sample_period.py`: simple `ResponsePort` plus `uint16` setter pattern.
  - `src/labbench_comm/devices/lio/functions/reset_calibration.py`: stale code `0x43` function not listed in the IDD.
  - `src/labbench_comm/devices/lio/functions/__init__.py` and `src/labbench_comm/devices/lio/__init__.py`: public exports.
  - `tests/devices/lio/test_lio_central.py`: LIO function shape and export tests.
- **External or internal references:**
  - IDD `GET_ENDIANNESS` (`0x03`): request length `0`, response length `2`, offset `0` `uint16` endian marker, always `1`.
  - IDD `SET_INDICATORS` (`0x12`): request length `6`; offset `0` `uint8 ResponsePort`, offset `1` `uint8` LED bitfield, offset `2` `uint32` duration. Duration is parsed by firmware even though the analyzed sensor path forwards only LED state.
  - IDD `WRITE_CALIBRATION` (`0x41`): request length `13`; offset `0` `uint8 CalibratorID`, offset `1` valid marker, offsets `2` and `6` `int32` Q12 coefficients, offset `10` `uint16` maximum, offset `12` checksum.
  - IDD function summary does not include `0x43`.
- **Inputs, outputs, and contracts:**
  - New functions should use `_LIOFunction` and existing `Packet` field helpers.
  - Calibration coefficient float accessors should follow `ReadCalibration`: raw Q12 integer divided by `2 ** CALIBRATION_Q`; setters should write the raw integer for exact packet construction.
  - `WriteCalibration.valid_marker` should preserve the raw byte. A convenience boolean may be added only if raw-byte access remains available.
- **Environment assumptions:**
  - Python 3.12+ package, no new dependency needed.
- **Known constraints:**
  - The IDD is the source of truth. Do not silently keep unsupported LIO function codes as first-class public API.
  - EEPROM-writing functions can affect hardware; tests must stay packet-level and must not require connected devices.
- **Risks and edge cases:**
  - Removing a public export is potentially breaking. Keep the task scoped to the LIO package and update tests to reflect the IDD-backed surface.
  - `WriteCalibration` should not invent checksum calculation unless existing repo code already provides an IDD-compatible helper; packet accessors are enough for this task.

## Acceptance Criteria

- [x] `GetEndianness().code == 0x03`, request length is `0`, response length is `2`, and a response with bytes `01 00` decodes as marker `1`.
- [x] `SetIndicators().code == 0x12`, request length is `6`, response length is `0`, and setting port, LED bitfield, and duration writes offsets `0`, `1`, and `2..5` exactly as the IDD specifies.
- [x] `WriteCalibration().code == 0x41`, request length is `13`, response length is `0`, and all request fields map to the IDD offsets.
- [x] New function classes are importable from both `labbench_comm.devices.lio.functions` and `labbench_comm.devices.lio`.
- [x] `ResetCalibration` is no longer exported from `labbench_comm.devices.lio.functions` or `labbench_comm.devices.lio` unless implementation finds a newer IDD entry proving `0x43` is implemented; in that case the task notes the evidence in `Implementation Agent Notes`.
- [x] Unit tests cover the new packet shapes and public exports.

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

- **Suggested approach:** Add the three function modules, update exports, then adjust tests. Remove the stale `ResetCalibration` exports after verifying `rg -n "ResetCalibration|0x43" src tests examples` has no required internal use.
- **Preferred patterns/APIs:** Follow `_LIOFunction` subclasses and property patterns already used by `ReadCalibration`, `SetTimingSource`, and `SetSignalSamplePeriod`.
- **Files likely to change:** `src/labbench_comm/devices/lio/functions/*.py`, `src/labbench_comm/devices/lio/functions/__init__.py`, `src/labbench_comm/devices/lio/__init__.py`, and `tests/devices/lio/test_lio_central.py`.
- **Files likely not to change:** `src/labbench_comm/protocols/packet.py` and hardware integration tests.
- **Migration/rollout notes:** If removal of `ResetCalibration` is considered too breaking during implementation, keep a compatibility import only if it is clearly marked non-IDD and not included in `__all__`; document that decision in the task notes.
- **Testing notes:** Add tests that inspect raw request bytes, not hardware effects.
- **Potential blockers:** None.

## Validation Plan

- **Automated checks:**
  - `pytest -m unittest tests/devices/lio/test_lio_central.py`: validates new LIO function packet shapes, accessors, and exports.
  - `pytest -m unittest`: validates the broader unit suite still passes.
- **Manual checks:**
  - Inspect `src/labbench_comm/devices/lio/functions/__init__.py` and `src/labbench_comm/devices/lio/__init__.py` to confirm exported LIO functions line up with the IDD implemented function summary.
- **Regression checks:**
  - Confirm existing LIO function packet shape tests still pass for `ClearPrograms`, `GetAnalogSignal`, `GetEvent`, `GetInterfaceStatus`, and `ReadCalibration`.

## Implementation Agent Notes

Implemented in this task:

- Added `GetEndianness`, `SetIndicators`, and `WriteCalibration` LIO functions with IDD-backed packet codes, lengths, field offsets, and exports.
- Removed the stale `ResetCalibration` public API and deleted `src/labbench_comm/devices/lio/functions/reset_calibration.py` after confirming no internal `src`, `tests`, or `examples` references remained.
- Added unit coverage for packet shapes, field offsets, top-level and subpackage imports, and absence of `ResetCalibration` from public `__all__` lists.
- No README or example updates were needed: `rg -n "ResetCalibration|GET_ENDIANNESS|SET_INDICATORS|WRITE_CALIBRATION|GetEndianness|SetIndicators|WriteCalibration" README.md .documentation examples` found no stale README/example references, and the IDD already documents the functions.
- No lint, type-check, or formatting commands are configured in `pyproject.toml`, README, or `.github/workflows/ci.yml`.

Validation results:

- `pytest -m unittest tests/devices/lio/test_lio_central.py -k get_endianness`: passed.
- `pytest -m unittest tests/devices/lio/test_lio_central.py -k set_indicators`: passed.
- `pytest -m unittest tests/devices/lio/test_lio_central.py -k write_calibration`: passed.
- `pytest -m unittest tests/devices/lio/test_lio_central.py`: passed, 30 tests.
- `pytest -m unittest`: passed, 75 selected tests, 2 deselected. Pytest emitted a cache warning for `.pytest_cache`, but tests passed.
- `rg -n "GetEndianness|SetIndicators|WriteCalibration|ResetCalibration|0x43" src/labbench_comm/devices/lio tests/devices/lio/test_lio_central.py`: confirmed new exports/tests and no remaining `0x43` implementation.
- `python -m build`: first sandboxed attempt failed because isolated build dependency installation could not reach PyPI; rerun with approved network access passed and built `labbench_comm-0.1.2.tar.gz` and `labbench_comm-0.1.2-py3-none-any.whl`.
- `python -m twine check dist/*`: first sandboxed attempt failed with a permission error reading the built wheel; rerun with elevated permissions passed for both distributions.

Follow-ups:

- None.
