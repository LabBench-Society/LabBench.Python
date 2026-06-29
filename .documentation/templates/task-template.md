# Task Template

Use this template to create implementation-ready work issues. Remove this Task Template section when creating a task.

Follow `.documentation/planning/AGENTS.md` for IDs, filenames, statuses, and lifecycle rules.

## Issue Metadata

- **ID:** `T####`
- **Title:** `<imperative, specific, and outcome-oriented title>`
- **Status:** `Draft | Ready | In Progress | Blocked | Review | Done`
- **Type:** `Feature | Bug | Refactor | Test | Documentation | Chore`
- **Related Work:** `<links to issues, PRs, commits, docs, or "None">`

## Summary

`<1-3 sentences describing the requested outcome>`

## Problem Statement

- **Current behavior:** `<what happens now, with concrete examples when possible>`
- **Desired behavior:** `<what should happen after this task is complete>`
- **Why this matters:** `<business, user, reliability, maintainability, or compliance reason>`

## Scope

### In Scope

- `<specific deliverable or behavior>`
- `<specific file/module/API/workflow affected>`

### Out of Scope

- `<related work that should not be done in this task>`
- `<future enhancement or tempting refactor to avoid>`

## Context for Implementation Agent

Include only facts needed to implement the task.

- **Relevant files and directories:**
  - `<path>`: `<why it matters>`
- **Relevant existing patterns:**
  - `<pattern/helper/API/convention>`: `<how to use or preserve it>`
- **External or internal references:**
  - `<link or doc path>`: `<specific fact needed>`
- **Inputs, outputs, and contracts:**
  - `<API shape, event, schema, CLI behavior, UI state, data model, etc.>`
- **Environment assumptions:**
  - `<runtime, framework, feature flag, config, dependency, permissions>`
- **Known constraints:**
  - `<compatibility, performance, security, accessibility, rollout, migration, deadline>`
- **Risks and edge cases:**
  - `<case>`: `<expected handling>`

## Acceptance Criteria

- [ ] `<observable outcome that proves the main behavior works>`
- [ ] `<important edge case or failure mode is handled>`
- [ ] `<existing behavior that must be preserved>`
- [ ] `<required UX/API/error/documentation behavior>`

When behavior is scenario-based, use this format:

```gherkin
Given <initial state or precondition>
When <user or system action>
Then <expected observable result>
```

## Definition of Done

Mark non-applicable items as `N/A` with a short reason.

- [ ] All acceptance criteria pass.
- [ ] The implementation follows existing repository patterns and keeps the change scoped to this issue.
- [ ] Automated tests are added or updated for changed behavior, or a clear reason is documented for why tests are not appropriate.
- [ ] Relevant manual validation is completed and documented in this issue.
- [ ] Build, lint, type-check, formatting, and test commands relevant to the touched code pass.
- [ ] User-facing text, docs, configuration, examples, or migration notes are updated when behavior changes.
- [ ] Security, privacy, accessibility, performance, and compatibility implications were considered for the changed surface.
- [ ] No unrelated files, generated artifacts, or user changes are reverted or modified.
- [ ] Any follow-up work is explicitly listed with rationale.

## Implementation Notes

Provide guidance that reduces ambiguity without hiding requirements outside Acceptance Criteria.

- **Suggested approach:** `<short sequence of likely implementation steps>`
- **Preferred patterns/APIs:** `<existing helpers, abstractions, libraries, or conventions to use>`
- **Files likely to change:** `<paths, if known>`
- **Files likely not to change:** `<paths or areas to avoid, if useful>`
- **Migration/rollout notes:** `<data migration, feature flag, backward compatibility, release concern>`
- **Testing notes:** `<specific fixtures, test commands, scenarios, mocks, or manual checks>`
- **Potential blockers:** `<unknowns that must be resolved before implementation>`

## Validation Plan

List exact checks to run or perform.

- **Automated checks:**
  - `<command>`: `<what it validates>`
- **Manual checks:**
  - `<workflow or inspection>`: `<expected result>`
- **Regression checks:**
  - `<existing workflow that must still work>`: `<expected result>`

## Implementation Agent Notes

`<optional exceptional handoff notes not covered above; otherwise "None">`
