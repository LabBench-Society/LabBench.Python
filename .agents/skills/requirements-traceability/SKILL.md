---
name: requirements-traceability
description: Maintain the lightweight requirements and requirements-verification traceability workflow using templates in .documentation/templates/ and project-specific requirements/RVTM documents created from them. Use when adding, changing, deprecating, implementing against, or verifying explicit requirements, or when creating tests/manual evidence that should trace to requirements.
---

# Requirements Traceability

## Overview

Use this skill to keep requirements explicit, stable, and connected to verification evidence.

## Required Reading

1. Read the applicable `AGENTS.md` files.
2. Read `.documentation/AGENTS.md`.
3. If editing templates, read `.documentation/templates/AGENTS.md` and the template files in `.documentation/templates/`.
4. If maintaining live project requirements or verification evidence, read the project-specific requirements document and RVTM created from the templates.
5. If working from a planning task, read that task and `.documentation/planning/AGENTS.md`.

## Workflow

1. Identify whether the request changes requirements, implements behavior already covered by requirements, or adds verification evidence.
2. Do not invent product requirements. If the user or task does not provide enough behavior to write a requirement, ask or record the gap in the appropriate planning task.
3. Use stable `REQ-####` IDs. Never reuse an ID after deletion or deprecation.
4. Start new project-specific requirements and RVTM documents from `.documentation/templates/requirements.md` and `.documentation/templates/requirements-verification-traceability-matrix (RVTM).md`.
5. When adding or changing any requirement, including Draft requirements, add or update its RVTM row in the same change.
6. When adding automated or manual verification later, make the test/evidence reference the requirement ID and update the RVTM evidence fields.
7. Preserve deprecated requirements for traceability; mark them `Deprecated` and point to successor IDs when applicable.

## Requirement Rules

- Use requirements documents for behavior that future implementation, tests, or manual verification must satisfy.
- Use `.documentation/planning/tasks/` for task breakdown, design notes, broad research, and implementation plans.
- Requirement statuses are separate from planning task statuses; use only `Draft`, `Active`, and `Deprecated` for requirements.
- Keep each requirement human writable: one Markdown subsection with fixed fields from the template.
- Keep requirement text observable and testable. Prefer "The system shall..." phrasing.
- Do not describe implementation unless the implementation detail is itself required.
- Use `Draft`, `Active`, and `Deprecated` as requirement statuses:
  - `Draft`: proposed requirement; not ready to drive implementation or verification.
  - `Active`: current requirement that implementation and verification should satisfy.
  - `Deprecated`: historical requirement retained for traceability.
- Use the smallest useful requirement type: `Functional`, `Nonfunctional`, `Data`, `Interface`, `Operational`, or `Documentation`.
- Set `Status` to `Draft` unless the user, an accepted planning task, or an explicit project decision approves it as current behavior; approved current requirements are `Active`.
- Add a dated `Change History` bullet for every meaningful change.
- Preserve the requirement ID when clarifying without changing intent.
- Deprecate the old requirement and create a new ID when intent changes materially.
- When splitting a requirement, deprecate the original and create new child requirements.
- When merging requirements, keep the clearer surviving requirement Active, deprecate the other, and cross-reference both IDs.
- Fill `Deprecated Date`, `Reason`, and `Replaced By` when applicable.
- Planning tasks should reference requirement IDs when they implement, change, or verify explicit requirements.

## RVTM Rules

- Keep one RVTM row for every requirement in the project-specific requirements document.
- Update the RVTM in the same change as requirement additions, including Draft requirements, material changes, deprecations, or new verification evidence.
- Use `Unit`, `Integration`, `Manual`, `Inspection`, `Analysis`, or `Not Planned` as verification methods.
- Use `Not Planned`, `Planned`, `Implemented`, `Passed`, `Failed`, `Blocked`, or `Deprecated` as verification statuses.
- Do not create placeholder tests. Use `Not Planned` or `Planned` until real verification exists.
- Preserve rows for Deprecated requirements so historical evidence remains traceable.
- A requirement may have multiple verification methods; one verification asset may cover multiple requirements.
- If verification covers only part of a requirement, record the uncovered gap in the RVTM.
- When a requirement changes materially, review existing verification references before leaving its RVTM status as `Passed`.

## Verification Links

Use the lightest reference that will let a fresh agent find the evidence:

- Unit or integration tests: test file path plus test name, marker, assertion scope, or nearby `REQ-####` comment.
- Manual verification: dated evidence entry with requirement IDs, command/procedure, environment, actor, result, and artifact path when one exists.
- Inspection or analysis: dated note with the reviewed file, command, or reasoning artifact.

If no verification exists yet, mark the RVTM verification status as `Not Planned` or `Planned` rather than creating placeholder tests.
