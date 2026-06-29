# Documentation Agent Instructions

More specific `AGENTS.md` files override this file.

## Requirements

- Use `.agents/skills/requirements-traceability/SKILL.md` when adding, changing, deprecating, implementing against, or verifying requirements.
- Use `.documentation/templates/requirements.md` only as a template for project-specific requirements documents; do not record live requirements in template files.
- Use stable `REQ-####` IDs. Do not reuse IDs, and do not delete deprecated requirements needed for traceability.
- Do not invent product requirements from implementation ideas. If behavior is unclear, ask the user or record the gap in a planning task.
- Keep each requirement human writable: one Markdown subsection with fixed fields from the template.
- Use requirement statuses `Draft`, `Active`, and `Deprecated`.
- Requirement statuses are separate from planning task statuses; do not use planning statuses such as `Ready`, `In Progress`, `Blocked`, `Review`, or `Done` for requirements.
- Use requirement types `Functional`, `Nonfunctional`, `Data`, `Interface`, `Operational`, and `Documentation`; add a new type only when these are insufficient.
- Set `Status` to `Draft` unless the user, an accepted planning task, or an explicit project decision approves it as current behavior; approved current requirements are `Active`.
- Preserve the requirement ID when clarifying without changing intent.
- Deprecate the old requirement and create a new ID when intent changes materially, including splits. When merging, keep the clearer surviving requirement Active and deprecate the other.

## Verification testing

- Use `.documentation/templates/requirements-verification-traceability-matrix (RVTM).md` only as a template for project-specific RVTM documents; do not record live verification evidence in template files.
- Update the RVTM in the same change as any requirement addition, material requirement change, deprecation, or new verification evidence, including Draft requirements.
- Future unit, integration, and manual tests should reference requirement IDs when they verify explicit requirements.
- Do not create placeholder tests only to populate traceability. Record unplanned or planned verification honestly.
- Keep one RVTM row for every requirement in the project-specific requirements document.
- Use verification methods `Unit`, `Integration`, `Manual`, `Inspection`, `Analysis`, and `Not Planned`.
- Use verification statuses `Not Planned`, `Planned`, `Implemented`, `Passed`, `Failed`, `Blocked`, and `Deprecated`.
- Preserve RVTM rows for Deprecated requirements so historical evidence remains traceable.

## Planning

For `.documentation/planning/`, follow `.documentation/planning/AGENTS.md`. Do not duplicate or override planning status rules here.

Do not apply `.agents/skills/tdd/SKILL.md` to pure documentation-only edits.
