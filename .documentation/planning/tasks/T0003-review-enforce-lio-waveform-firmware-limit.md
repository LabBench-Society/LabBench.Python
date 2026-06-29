## Issue Metadata

- **ID:** `T0003`
- **Title:** `Enforce the LIO waveform firmware sample limit`
- **Status:** `Review`
- **Type:** `Bug`
- **Related Work:** `.documentation/documentation/lio/interface-design-description.md`

## Summary

Correct `SetWaveform` so it respects the firmware limit of `1000` samples documented by the IDD instead of allowing up to `1024`. Add tests that prevent constructing an over-limit waveform packet that the firmware would reject.

## Problem Statement

- **Current behavior:** `src/labbench_comm/devices/lio/functions/set_waveform.py` defines `MAXIMUM_NUMBER_OF_INSTRUCTIONS = 1024` and uses `sample_count = min(len(self.samples), self.MAXIMUM_NUMBER_OF_INSTRUCTIONS)`. The IDD says the firmware rejects sample counts greater than `MAXIMAL_NUMBER_OF_SAMPLES` (`1000`), and specifically notes CommLib's `1024` value is not authoritative.
- **Desired behavior:** The Python LIO waveform encoder uses `1000` as the authoritative maximum sample count and does not silently construct packets with `1001..1024` samples.
- **Why this matters:** A host can currently send waveform packets that the firmware rejects as too long. Silent truncation also risks driving a waveform different from the caller's intended signal.

## Scope

### In Scope

- Update `SetWaveform` maximum sample count to `1000`, using an IDD-aligned constant name if helpful.
- Decide and implement the safest existing-style behavior for over-limit input. Prefer raising `ValueError` for more than `1000` samples to avoid silently changing output; if preserving silent truncation is chosen for consistency, document that choice in implementation notes and ensure no packet can contain more than `1000` samples.
- Ensure `period` validation uses the encoded sample count and cannot accept a non-zero period that is shorter than `offset + sample_count`.
- Add or update unit tests for exactly `1000` samples and `1001` samples.

### Out of Scope

- Changing waveform normalized sample scaling (`-1..+1` to `-4095..+4095`) because it already matches the IDD.
- Changing `SetStimulusProgram` or `SetTriggerSequence` maximum counts.
- Hardware validation with a connected LIO.

## Context for Implementation Agent

- **Relevant files and directories:**
  - `src/labbench_comm/devices/lio/functions/set_waveform.py`: contains the incorrect `MAXIMUM_NUMBER_OF_INSTRUCTIONS = 1024` constant and packet construction.
  - `tests/devices/lio/test_lio_central.py`: contains `test_set_voltage_and_waveform_dynamic_packets`.
- **External or internal references:**
  - IDD `SET_WAVEFORM` summary: request length is `6 + 2 * n`, where `0 <= n <= 1000`.
  - IDD `SET_WAVEFORM` implemented constraints: sample count must be at most `MAXIMAL_NUMBER_OF_SAMPLES` (`1000`).
  - IDD construction guidance: "Treat the firmware limit of `1000` samples as authoritative. CommLib contains a `MaximumNumberOfInstructions` value of `1024` for `SetWaveform`, but the firmware rejects sample counts greater than `MAXIMAL_NUMBER_OF_SAMPLES` (`1000`)."
- **Inputs, outputs, and contracts:**
  - A waveform with exactly `1000` samples should produce request length `2006`.
  - A waveform with `1001` samples must not produce a packet with request length `2008`.
  - Samples should continue to encode as signed little-endian `int16` values, with normalized `-1.0`, `0.0`, and `1.0` mapping to `-4095`, `0`, and `4095`.
- **Environment assumptions:**
  - No new dependencies are required.
- **Known constraints:**
  - Keep behavior scoped to host packet construction. Do not modify firmware-facing protocol framing.
- **Risks and edge cases:**
  - If the previous silent truncation behavior is relied on by callers, raising `ValueError` is a breaking behavior change. The IDD-backed safety reason should be captured in tests and, if docs mention waveform limits, docs should be updated.

## Acceptance Criteria

- [x] `SetWaveform` uses `1000` as its maximum sample count for packet construction.
- [x] A waveform with exactly `1000` samples can be encoded and produces a packet length of `2006`.
- [x] A waveform with `1001` samples does not produce an over-limit request packet; the preferred behavior is a clear `ValueError`.
- [x] Existing waveform fields still encode correctly: repeat at offset `0`, offset at `2`, period at `4`, and samples starting at `6`.
- [x] Existing sample scaling and period-shorter-than-waveform validation behavior is preserved or made stricter only where needed to prevent firmware-rejected packets.

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

- **Suggested approach:** Rename or replace `MAXIMUM_NUMBER_OF_INSTRUCTIONS` with a sample-count constant set to `1000`, check `len(self.samples)` before building the packet, and update tests.
- **Preferred patterns/APIs:** Keep using `Packet`, `insert_uint16`, `insert_int16`, and existing `UpdateRate` conversion helpers.
- **Files likely to change:** `src/labbench_comm/devices/lio/functions/set_waveform.py` and `tests/devices/lio/test_lio_central.py`.
- **Files likely not to change:** Other LIO function modules and protocol packet code.
- **Migration/rollout notes:** If raising `ValueError`, use a message that states the firmware limit of `1000` samples.
- **Testing notes:** Add one focused test for `1000` samples and one for `1001` samples. Keep the existing small waveform test.
- **Potential blockers:** None.

## Validation Plan

- **Automated checks:**
  - `pytest -m unittest tests/devices/lio/test_lio_central.py`: validates waveform packet construction and LIO regression coverage.
  - `pytest -m unittest`: validates the broader unit suite still passes.
- **Manual checks:**
  - Inspect the `SetWaveform` constant and packet length calculation to confirm no request packet can contain more than `1000` samples.
- **Regression checks:**
  - Confirm the existing four-sample waveform test still maps `[-2.0, 0.0, 0.5, 2.0]` to `-4095`, `0`, approximately half scale, and `4095`.

## Implementation Agent Notes

- Implemented by raising `ValueError` before packet construction when `len(samples) > 1000`; this prevents silently changing caller-provided waveforms and prevents firmware-rejected packets.
- Added boundary tests for `1000` samples, `1001` samples, and a non-zero period shorter than `offset + sample_count`; kept the existing small waveform packet/scaling regression.
- Manual inspection confirmed `SetWaveform.MAXIMUM_SAMPLE_COUNT = 1000`, request length uses `(sample_count + 3) * 2`, and `period` validation uses `offset + sample_count`.
- `rg -n "1024|MaximumNumberOfInstructions|MAXIMUM_NUMBER_OF_INSTRUCTIONS|SetWaveform|SET_WAVEFORM|waveform" README.md .documentation src tests`: no stale user-facing `1024` waveform limit found outside the task context; IDD already documents `1000`.
- `pytest -m unittest tests/devices/lio/test_lio_central.py -k "more_than_firmware_sample_limit"` initially failed as expected before implementation because `ValueError` was not raised.
- `pytest -m unittest tests/devices/lio/test_lio_central.py -k "more_than_firmware_sample_limit"`: passed, 1 selected test.
- `pytest -m unittest tests/devices/lio/test_lio_central.py -k "waveform"`: passed, 4 selected tests, with one pytest cache warning.
- `pytest -m unittest tests/devices/lio/test_lio_central.py`: passed, 33 tests, with one pytest cache warning.
- `pytest -m unittest`: passed, 78 selected tests and 2 deselected, with one pytest cache warning.
- `python -m build`: first failed in the sandbox because isolated build dependency installation could not reach PyPI; rerun with approved network escalation passed and built `labbench_comm-0.1.2.tar.gz` and `labbench_comm-0.1.2-py3-none-any.whl`.
- No lint, type-check, or formatter command is configured in `pyproject.toml`; no separate command was run.
- Security, privacy, accessibility, performance, and compatibility implications were considered. Compatibility impact is limited to rejecting previously accepted over-limit inputs that firmware rejects.
- Follow-ups: none.
