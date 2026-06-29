---
name: implement-ready-tasks
description: Implement all Markdown planning tasks with `Status: Ready`. Use when Codex is asked to implement all ready tasks, keep taking ready tasks, run the ready-task queue, batch implement planning tasks, or perform AFK/subagent execution of ready tasks from .documentation/planning/tasks.
---

# Implement Ready Tasks

Implement tasks whose metadata has `Status: Ready` and whose filenames match `.documentation/planning/tasks/T*-ready-*.md`. This repo has tasks, not milestones.

## Workflow

1. Read `.documentation/planning/AGENTS.md`.
2. Discover ready tasks with `rg --files .documentation/planning/tasks | rg "T[0-9]{4}-ready-"`.
3. Select the first ready task in task ID order.
4. Stop successfully if no ready tasks remain.
5. Resolve the task ID to its matching `tasks/T####-ready-*.md` file.
6. Implement exactly one selected task using `.agents/skills/implement-task/SKILL.md`.
7. Verify the task status, filename, recorded validation, and commit result before selecting another task.
8. Stop on the first task that becomes `Blocked`, fails validation, is incomplete, or has an unsafe task/repo contradiction.
9. Continue until no ready tasks remain or a stop condition occurs.

## Execution Mode

- Use worker subagents to implement tasks.
- Spawn one fresh worker per task and wait for it before selecting the next task.
- Workers must not spawn, delegate to, resume, wait on, or close other agents.
- If worker subagent tooling is unavailable, stop before implementation and report that as a blocker.

## Worker Prompt

Give each worker one task:

```text
Implement planning task T#### in <workspace>.

Read .documentation/planning/AGENTS.md first. Use .agents/skills/implement-task/SKILL.md.

Do not spawn or delegate to other agents. Implement only this task's In Scope work and Acceptance Criteria. Follow the planning status rules and record validation results in the task.

Report:
- task ID
- final status
- commit hash or why no commit was needed
- files changed
- validation commands and results
- blockers, risks, or follow-ups
- confirmation that no subagents were spawned
```

## Parent Verification

After each task:

- Read the task file and verify status, filename, validation results, and commit/no-commit result.
- Success means the task is `Review`, or `Done` only when explicit review or acceptance is recorded in the task.
- If the task is `Blocked`, stop and report the blocker.
- If validation failed or work is incomplete, stop and report the failing condition.

## Final Report

Report:

- tasks completed in this run
- stop reason
- final status per selected task
- commit hash per completed task when available
- validation summary
- remaining ready tasks or blockers
