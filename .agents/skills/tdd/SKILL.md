---
name: tdd
description: Test-driven development with red-green-refactor loop for executable behavior changes. Use when implementing code features, bug fixes, behavior refactors, integration tests, test-first work, or tasks whose Definition of Done requires tests. Do not use for pure documentation, planning, template, or text-only tasks unless they change executable validation behavior.
---

# Test-Driven Development

## Applicability

Use TDD for code behavior changes. Do not apply TDD to pure documentation, planning, template, or text-only tasks.

For planning tasks, derive test behaviors from the task's Acceptance Criteria and Validation Plan. If requirements are unsafe, contradictory, or missing, follow `.documentation/planning/AGENTS.md`.

Keep TDD changes scoped to the requested behavior. Refactor only touched code or code that must change to make the tested behavior pass; do not introduce architectural changes unless the prompt or planning task requires them. Refactor guidance in this skill is subordinate to repository instructions that prohibit unrequested architecture changes.

## Philosophy

**Core principle**: Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests should not.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe what the system does, not how it does it. A good test reads like a specification. These tests survive refactors because they do not care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means instead of the public interface. If a refactor breaks tests while behavior is unchanged, those tests were probably testing implementation.

See [`./tests.md`](./tests.md) for examples and [`./mocking.md`](./mocking.md) for mocking guidelines.

## Anti-Pattern: Horizontal Slices

Do not write all tests first, then all implementation. That is horizontal slicing.

Correct approach: vertical slices via tracer bullets. One test, one implementation, repeat. Each test responds to what you learned from the previous cycle.

```text
WRONG:
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT:
  RED -> GREEN: test1 -> impl1
  RED -> GREEN: test2 -> impl2
  RED -> GREEN: test3 -> impl3
```

## Workflow

### 1. Planning

When exploring the codebase, use project vocabulary so test names and interface language match the codebase.

For planning tasks, the task replaces plan approval: use Acceptance Criteria and Validation Plan as the behavior list.

For non-task requests, clarify only what is needed:

- [ ] Public interface changes
- [ ] Behaviors to test first
- [ ] Relevant constraints or edge cases

Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer Bullet

Write one test that confirms one behavior:

```text
RED:   Write test for first behavior -> test fails
GREEN: Write minimal code to pass -> test passes
```

This proves the path works end-to-end.

### 3. Incremental Loop

For each remaining behavior:

```text
RED:   Write next test -> fails
GREEN: Minimal code to pass -> passes
```

Rules:

- One test at a time.
- Only enough code to pass the current test.
- Do not anticipate future tests.
- Keep tests focused on observable behavior.

### 4. Refactor

After all tests pass, look for refactor candidates in [`./refactoring.md`](./refactoring.md):

- [ ] Extract duplication.
- [ ] Deepen modules where it simplifies the public interface.
- [ ] Apply SOLID principles where natural.
- [ ] Run tests after each refactor step.

Never refactor while RED. Get to GREEN first.

## Checklist Per Cycle

```text
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Code is minimal for this test
[ ] No speculative features added
```
