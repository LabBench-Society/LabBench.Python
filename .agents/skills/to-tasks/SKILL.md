---
name: to-tasks
description: Break complex work into independently-grabbable Markdown tasks under .documentation/planning/tasks, or harden/revise an existing task into a fresh-agent-ready implementation spec. Use when user wants to convert a plan into tasks, break down work, create implementation tasks, analyze a task for side effects, or revise a task with context, acceptance criteria, definition of done, implementation notes, and validation plan.
---

# To Tasks

Break a plan into independently-grabbable tasks using vertical slices (tracer bullets), or harden one existing task so a fresh agent can implement it safely.

## Process

### 1. Gather Context

Work from whatever is already in the conversation context. If the user passes a task reference, read the referenced Markdown task file directly. If the reference is a title or short name, search `.documentation/planning/tasks/`.

If the user asks to revise, improve, analyze, or harden one existing task, use **Task hardening mode**. Do not split into new tasks unless asked.

If the user asks to break down, decompose, or convert work into tasks, use **Task breakdown mode**.

### 2. Explore The Codebase

For code tasks, inspect current code before writing tasks or plans. Treat code as requirements.

Do the smallest useful investigation:

- Read related completed tasks and docs.
- Search source/tests with `rg`.
- Read current classes, call sites, UI/view-models, templates, validation, persistence, and tests touched by the behavior.
- Use project domain vocabulary and respect ADRs in the area.

Skip code exploration only for pure documentation/admin tasks or when the user explicitly supplies enough current context.

### 3. Task Hardening Mode

Revise the existing Markdown task file using `.documentation/templates/task-template.md` and `.documentation/planning/AGENTS.md`.

Produce or update:

- **Summary and Problem Statement**: current problem, target behavior, and why it matters.
- **Scope**: explicit in-scope and out-of-scope boundaries.
- **Context for Implementation Agent**: related tasks, files, tests, docs, contracts, assumptions, constraints, risks, and edge cases.
- **Acceptance Criteria**: outcome-based and testable.
- **Definition of Done**: applicable quality gates from the template.
- **Implementation Notes**: suggested approach, preferred patterns/APIs, likely files, testing notes, blockers.
- **Validation Plan**: automated, manual, and regression checks.

For code tasks, consider affected surfaces such as validation, runtime lifecycle, serialization, UI, templates, persistence, edge cases, and existing tests. Resolve ambiguous product decisions in the task or mark them as blockers.

Before setting a task `Ready`, confirm:

- [ ] The task follows `.documentation/planning/AGENTS.md`.
- [ ] The title is specific enough to understand the expected outcome from an issue list.
- [ ] The summary and problem statement explain why the work is needed.
- [ ] The scope has clear in-scope and out-of-scope boundaries.
- [ ] The context section includes applicable repository facts needed for implementation.
- [ ] Acceptance criteria are observable and testable.
- [ ] Definition of Done is applicable to the repository and not a substitute for acceptance criteria.
- [ ] Implementation notes guide the fresh agent without hiding requirements outside acceptance criteria.
- [ ] Validation commands are exact, or the task states how the implementation agent should discover them.
- [ ] Unknowns are resolved for `Ready`; unresolved blockers are recorded and the task remains `Blocked`.

### 4. Task Breakdown Mode

Break the plan into **tracer bullet** tasks. Each task is a thin vertical slice that cuts through all integration layers end-to-end, not a horizontal slice of one layer.

Slices may be ready or blocked. Treat these as proposed statuses until applying the planning status rules.

<vertical-slice-rules>
- Each slice delivers a narrow but COMPLETE path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
</vertical-slice-rules>

### 5. Approval Gate

Before writing task files for a multi-task breakdown, present the proposed hardening plan or task breakdown and ask for approval unless the user explicitly asked to revise or publish now.

For task breakdowns, present a numbered list. For each slice, show:

- **Title**: short descriptive name
- **Proposed status**: Ready / Blocked
- **Blocked by**: which other slices (if any) must complete first
- **User stories covered**: which user stories this addresses (if the source material has them)

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Are the dependency relationships correct?
- Should any slices be merged or split further?
- Are the correct slices proposed as Ready or Blocked?

Iterate until the user approves the breakdown.

### 6. Write Markdown Tasks

For each approved slice, create or update a Markdown task in `.documentation/planning/tasks/`. Use `.documentation/templates/task-template.md` as the schema and `.documentation/planning/AGENTS.md` as the workflow authority.

Write tasks in dependency order (blockers first) so dependent tasks can reference stable task IDs and filenames in `Related Work`, `Context for Implementation Agent`, or `Potential blockers`.

Follow `.documentation/planning/AGENTS.md` for task IDs, section placement, status changes, and filename rules. Read back each task file after writing to verify the content is complete and valid Markdown.
