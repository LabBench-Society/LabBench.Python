# Planning Agent Instructions

This file is the authority for planning task IDs, filenames, statuses, and lifecycle rules.

Use `.documentation/templates/task-template.md` for planned work items. Store tasks under `.documentation/planning/tasks/` using status-bearing filenames:

```text
T####-status-short-kebab-title.md
```

Filename status slugs map to task metadata statuses as follows:

| Filename Slug | Metadata Status |
| --- | --- |
| `draft` | `Draft` |
| `ready` | `Ready` |
| `in-progress` | `In Progress` |
| `blocked` | `Blocked` |
| `review` | `Review` |
| `done` | `Done` |

The task metadata `Status` is canonical. The filename slug must match it so agents can discover tasks without a separate index. In prose, `implementation-ready` means `Status: Ready` and filename slug `ready`; do not use `Ready for Implementation`.

## Core Rules

- Write for a fresh implementation agent with no chat history.
- Include the repository facts needed to do the work: paths, commands, contracts, observed output, constraints, and minimal rationale.
- Exclude full design documents, unrelated meeting notes, speculation, and broad background.
- Prefer testable outcomes over implementation preferences unless the implementation detail is required.
- Use Section Mapping to place task content.
- If information is unknown, either research it, inspect the repo, or mark it as a blocker.
- A task is the source of truth for intended behavior; the repository is the source of truth for current state. If they conflict, update the task or stop for clarification when the safe requirement cannot be inferred.

## Section Mapping

| Section | Put Here |
| --- | --- |
| `Issue Metadata` | ID, title, status, type, and related work. |
| `Summary` | One to three sentences describing the requested outcome. |
| `Problem Statement` | Current behavior, desired behavior, and why the change matters. |
| `Scope` | In-scope deliverables and explicit out-of-scope boundaries. |
| `Context for Implementation Agent` | Repository facts: paths, commands, contracts, constraints, observed output, and minimal rationale. |
| `Acceptance Criteria` | Required testable outcomes, including every must-have behavior. |
| `Definition of Done` | Shared completion and quality gates; no new feature requirements. |
| `Implementation Notes` | Suggested approach, preferred patterns, likely files, risks, testing hints, and blockers. |
| `Validation Plan` | Exact checks to run and expected results. |
| `Implementation Agent Notes` | Exceptional handoff notes not covered by the sections above. |

Keep requirements in Acceptance Criteria, preferences in Implementation Notes, facts and commands in Context or Validation Plan, and completion gates in Definition of Done.

## Creating a Task

1. Re-read existing `tasks/T*.md` filenames.
2. Assign the next unused task ID.
3. Copy `.documentation/templates/task-template.md` into a `draft` task file.
4. Fill metadata with ID, specific imperative title, status, type, and related work.
5. Inspect relevant repository files before writing Context for Implementation Agent.
6. Define scope, observable acceptance criteria, implementation notes, and validation checks.
7. Apply status changes with the status table below.

## Hardening a Draft

- Remove filler, duplicated context, and solution speculation that does not affect implementation.
- Ensure every acceptance criterion can be verified by test, command, UI/API behavior, or documented inspection.
- Record repository-specific patterns, risks, edge cases, migrations, feature flags, permissions, and compatibility requirements only when relevant.
- Keep links specific to the fact needed; do not ask the implementer to reread broad documents unnecessarily.
- Before setting `Ready`, confirm there are no unresolved blockers and a fresh agent can implement from the task and repo.

## Implementing a Task

1. Read the task first, then inspect the repository paths and patterns it names.
2. Apply status changes with the status table below.
3. Keep changes scoped to In Scope and Acceptance Criteria.
4. Update checklist items only after verifying them.
5. Record actual validation commands and results in the task.

## Updating Tasks

- Keep updates factual and compact: changed scope, new constraints, validation results, blockers, or follow-up work.
- Do not rewrite completed context unless it is wrong or misleading.
- When scope changes, update In Scope, Out of Scope, Acceptance Criteria, and Validation Plan together.
- Apply status changes with the status table below.

## Definitions

- `task ID`: stable unique ID in `T####` format. Use the next unused number found across `tasks/T*.md`; never reuse or change an ID after creation.
- `task filename`: status-bearing filename in `T####-status-short-kebab-title.md` format. The ID must match task metadata, and the status slug must match task metadata `Status`.
- `ready task discovery`: find implementation-ready tasks with `rg --files .documentation/planning/tasks | rg "T[0-9]{4}-ready-"` and select tasks in task ID order.

## Status Transition Rules

This table is the only authority for task status changes. Update task metadata and filename slug in the same change.

| Status | Set When | Required Before Setting |
| --- | --- | --- |
| `Draft` | A task is being created or hardened and is not ready for implementation. | Task file exists from the template with required metadata started. |
| `Ready` | A fresh agent can implement using only the task and repo. | The task has a specific title, clear scope, needed context, observable acceptance criteria, applicable Definition of Done, implementation notes, validation commands or discovery steps, and no unresolved blockers. |
| `In Progress` | An implementation agent starts work. | Agent has read the task and inspected referenced repo context. |
| `Blocked` | Progress requires missing information, a human decision, an external dependency, or resolving an unsafe task/repo contradiction. | The blocker and needed decision or change are recorded in the task. |
| `Review` | Implementation is complete and ready to inspect. | Acceptance criteria pass, applicable Definition of Done items are complete, and actual validation commands/results are recorded. |
| `Done` | Work is reviewed or accepted according to project workflow. | Review or acceptance is explicitly recorded in the task. Implementation agents normally stop at `Review` unless the user or task provides explicit acceptance. |
