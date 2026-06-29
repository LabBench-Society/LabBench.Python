# Repository Agent Instructions

More specific `AGENTS.md` files override this file.

# Purpose

The purpose of the library is to implement a communications library for LabBench devices.

# Content

This is a Python 3.12+ `src/` package named `labbench_comm`, with typed package metadata (`py.typed`) and a very small CLI that currently only exposes `labbench-comm --version`. The public substance is the library API, not the CLI.

The core runtime stack is layered as:

- `serial`: `PySerialIO` wraps pyserial with non-blocking reads; `AsyncSerialConnection` owns the async lifecycle, background reader task, and async writes.
- `protocols`: `Frame`/`Destuffer` implement DLE/STX/ETX byte framing, `Packet` implements compact and extended packet layouts with optional address and additive/CRC8-CCITT checksums, `BusCentral` serializes request/response function execution and dispatches unsolicited messages, and `Device` adds retry, identification, ping, error-string, and async-context-manager behavior.
- `devices`: concrete CPAR+ and LabBench I/O device packages provide enums, packet codecs, `DeviceFunction` subclasses, `DeviceMessage` subclasses, and central classes that maintain latest device state plus callback lists.

Protocol conventions matter for most changes: function packets use codes below `0x80`; unsolicited messages use codes at or above `0x80`; error/NAK packets use code `0x00`; numeric packet helpers are little-endian unless `Packet.reverse_endianity` is explicitly set; payload bytes equal to DLE (`0xFF`) are escaped at the frame layer.

Supported device surfaces are:

- CPAR+: `CPARplusCentral` targets manufacturer `InventorsWay`, device id `4`, baudrate `38400`, status/event messages, operating mode and waveform-program functions, a 6-byte waveform instruction codec, stimulation-state tracking, captured stimulation samples, and an optional background ping loop used as a stimulation dead-man mechanism.
- LIO: `LIOCentral` targets manufacturer `InventorsWay`, device id `2`, firmware major version `>= 2`, baudrate `57600`, status/event/signal/button/trigger/analog/threshold messages, response-port state tracking, calibration/event access, waveform/stimulus/trigger-sequence output functions, direct voltage and interface logic functions, and callback lists for incoming message types.

The examples are hardware workflows, not isolated sample snippets. LIO examples cover identification, input monitoring, analog reads, voltage output, stimulus programs, waveform output, trigger sequences, and calibration/event records. CPAR+ examples cover pressure stimulus workflows and plotting stimulation data. Output-driving examples can actuate connected hardware.

Tests are split by intent: `pytest -m unittest` covers packet/frame behavior, message dispatch, async serial lifecycle, LIO function/message packet shapes and scaling, CPAR waveform encoding boundaries, and package version metadata. `pytest -m hardware` is for connected-device integration, including generic identification and CPAR+ hardware checks.

`.documentation/documentation/lio/interface-design-description.md` is a detailed LIO ECP reference derived from firmware/CommLib evidence. Use it when changing LIO packet layouts, message fields, function codes, or semantics; do not treat the root README as the protocol authority.


# Overall rules

Your job is to assist a human writing code and documentation.

Change only the minimal code needed to implement the prompt or task.

- Treat code as requirements. Do not change architecture or code unless explicitly requested by a prompt or task.
- When finishing implementation work, commit changed repo files unless the user explicitly says not to commit. Use the task title plus implementation notes for the commit message when implementing a planning task.
- At the end of every agent turn that performed work or analysis, always play a beep using:
  
  ```PowerShell
  C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -Command "[console]::Beep(800, 200)"
  ```
Run the exact command above with escalated shell permissions directly so it is not attempted inside the filesystem sandbox first. Keep the `-Command` argument quoted so PowerShell parses `Beep(800, 200)` as a method call. This applies regardless of outcome: completed, blocked, failed, documentation-only, or analysis-only. The beep is notification only, not validation or task status.

## Coding style

- Prefer simple, explicit, and readable code over clever or highly abstract solutions. 
- Optimise for maintainability and ease of understanding by a new developer. 
- Keep functions small and focused. 
- Avoid premature optimisation, unnecessary patterns, deep inheritance, and over-engineering. Use clear naming and straightforward control flow. 
- Complexity must be justified by a concrete requirement.

## Repo search

Use `rg`/`rg --files` for read-only repository discovery before slower alternatives.

- Find files: `rg --files`
- Find task IDs: `rg -n "T0001|T####" .documentation/planning/tasks`
- Find task statuses: `rg --files .documentation/planning/tasks`
- Find ready tasks: `rg --files .documentation/planning/tasks | rg "T[0-9]{4}-ready-"`
- Find code references: `rg -n "ClassName|methodName|configKey" src tests`
- Audit stale terms: `rg -n "Backlog|milestone|AFK" .documentation .agents`
- Check TODOs/follow-ups: `rg -n "TODO|follow-up|Blocked" .`

## Pull requests

- Never make or merge pull requests.
- When asked to write text for pull requests, always write the title and description in two separate text boxes that can be copy pasted.
- When asked to write text it is always assumed that it will be for all the work performed on the current branch.

## Dependencies

Prefer mature, well-respected, actively maintained, and well-documented libraries over in-house code when they fit the requirement and reduce long-term maintenance risk.

Do not add dependencies silently, instead add a planning task that contains:

- The dependency name, intended package source, and maturity signals such as documentation quality, maintenance activity, adoption, and ecosystem fit.
- Which project or projects would reference it.
- Why the dependency is needed and why it is preferred over existing code or new in-house code.
- Reasonable alternatives, including in-house implementation when relevant, and the impact of not adding the dependency.
- Compatibility, licensing, security, maintenance, and cleanroom implications relevant to this repository.

If the dependency is already explicitly approved by the user or by a planning task with `Status: Ready`, it may be added as part of that work. 

# Inbox

Documents and material may be placed in `.inbox/` by the user. Use it as source input when creating tasks; move it only when the prompt or task explicitly asks.

### Internal documentation

Internal documentation lives in `.documentation/`.

When creating, updating, auditing, or reorganizing repository documentation, use `.agents/skills/documentation-writer/SKILL.md`.

## Requirements and Verification Traceability

For work that adds, changes, implements, or verifies explicit product or system requirements, use `.agents/skills/requirements-traceability/SKILL.md` for the lightweight requirements/RVTM workflow. Templates live in `.documentation/templates/requirements.md` and `.documentation/templates/requirements-verification-traceability-matrix (RVTM).md`; do not record live requirements or evidence in template files. Do not claim regulatory compliance or create a broader quality-management system.

## Planning Tasks

Read `.documentation/planning/AGENTS.md` for the planning task workflow. Route task work to the right skill:

- Create, break down, revise, or harden tasks: `.agents/skills/to-tasks/SKILL.md`
- Implement one task: `.agents/skills/implement-task/SKILL.md`
- Implement all ready tasks: `.agents/skills/implement-ready-tasks/SKILL.md`
- Executable behavior changes: `.agents/skills/tdd/SKILL.md`

Do not use TDD for pure documentation tasks.
