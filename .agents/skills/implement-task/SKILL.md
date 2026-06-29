---
name: implement-task
description: Implement one existing Markdown planning task by ID or path. Use when Codex is asked to execute, work on, complete, validate, review-readiness, or continue a task from .documentation/planning/tasks, especially references like T0001 or tasks/T0001-name.md.
---

# Implement Task

Implement exactly one existing task from `.documentation/planning/tasks/`.

## Workflow

1. Read `.documentation/planning/AGENTS.md`.
2. Resolve the task:
   - If given `T####`, find it in `tasks/T####-*.md`.
   - If given a path, read that file and verify its `ID` metadata matches the filename.
3. Read the full task before editing code.
4. Apply task status changes through the planning status rules.
5. Inspect the repository paths, commands, contracts, and constraints named in the task.
6. Implement only the task's In Scope work and Acceptance Criteria.
7. For executable behavior changes or tasks requiring tests, use `.agents/skills/tdd/SKILL.md`; skip TDD for pure documentation tasks.
8. Update task checklists only after verification.
9. Record actual validation commands and results in the task.
10. Follow the repository commit policy and record the commit hash or why no commit was needed.

## Guardrails

- If the task and repository conflict, follow `.documentation/planning/AGENTS.md`.
- If required context is missing, inspect the repo first; use `Blocked` only when progress depends on missing information or an external decision.
- Keep task edits factual and compact: status, checklist progress, validation results, blockers, and follow-ups.
- Do not change task ID after creation.
