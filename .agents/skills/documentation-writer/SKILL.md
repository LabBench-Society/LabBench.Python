---
name: documentation-writer
description: Create, update, audit, or reorganize repository documentation with evidence-based, minimal-churn edits. Use when Codex is asked to write README content, internal documentation under .documentation/, AGENTS.md guidance, architecture/explanation docs, API/CLI/config references, troubleshooting guides, changelogs, migration notes, or agent-readable documentation maps, while keeping implemented, documented, tested, planned, inferred, and unknown behavior clearly separated.
---

# Documentation Writer

## Overview

Write documentation as a careful technical maintainer. Prefer accurate, traceable, minimal edits over polished prose that is not grounded in the repository.

This skill covers general documentation work. For specialized workflows, use the repo-specific authority first:

- Requirements or RVTM work: read `.agents/skills/requirements-traceability/SKILL.md`.
- Planning task creation, hardening, or status changes: read `.documentation/planning/AGENTS.md` and use `.agents/skills/to-tasks/SKILL.md`.
- Implementing planning tasks: use `.agents/skills/implement-task/SKILL.md`.
- Pure documentation edits do not require `.agents/skills/tdd/SKILL.md`.

## Required Reading

1. Read the applicable `AGENTS.md` files before editing.
2. Read existing documentation that is likely to be touched.
3. When documenting current behavior, inspect the relevant source, tests, examples, configuration, scripts, API definitions, or CLI help.
4. When documenting intended behavior, inspect requirements, ADRs, planning tasks, or explicit user decisions.

Do not document behavior from the user request alone unless the request is explicitly for a draft, proposal, or brainstorming artifact.

## Repository Homes

Prefer existing homes and preserve their structure:

- `README.md`: project orientation and quick start.
- `AGENTS.md`: repository-wide agent instructions.
- `.documentation/`: internal documentation, requirements, verification, planning, and templates.
- `.documentation/documentation/`: general documentation about the project.
- `.documentation/requirements/`: project-specific requirements documents created from templates.
- `.documentation/verification/`: verification evidence and traceability artifacts.
- `.documentation/planning/tasks/`: planning tasks governed by `.documentation/planning/AGENTS.md`.
- `.agents/skills/`: repo-local skills.
- `llms.txt`: concise AI-readable documentation map, if the repo uses one.

Create a new file only when no existing file is the right home, the content has a distinct audience or purpose, or the existing file would become confusing.

## Evidence Labels

Use labels when they prevent future readers or agents from confusing facts, plans, and guesses:

```text
[IMPLEMENTED] Verified from source code or runtime behavior.
[DOCUMENTED] Stated in existing project documentation.
[TESTED] Verified by automated or manual tests.
[PLANNED] Described in planning, roadmap, issue, or requirements material.
[INFERRED] Reasonable inference from code or structure, but not explicitly stated.
[UNKNOWN] Not enough evidence.
[TODO-HUMAN] Requires a human decision.
[DEPRECATED] Present but marked obsolete or superseded.
[CONFLICT] Repository sources disagree.
```

Use labels freely in agent-facing docs, requirements notes, migration notes, audits, and planning documentation. For end-user docs, keep the prose readable, but still avoid unsupported claims.

## Workflow

1. Determine the documentation task: create, update, audit, summarize behavior, explain architecture, document API/CLI/config, update agent guidance, write troubleshooting, or remove stale information.
2. Identify the primary audience: users, developers, maintainers, future agents, API consumers, testers, operators, or planning stakeholders.
3. Classify the document type:
   - Tutorial: guided learning path.
   - How-to: steps to complete a task.
   - Reference: exact API, CLI, schema, config, file format, or error behavior.
   - Explanation: architecture, rationale, concepts, tradeoffs, or lifecycle.
   - Agent guidance: repository-specific instructions for future coding agents.
4. Build an internal evidence map for important claims:

```text
Claim:
Evidence:
Status: IMPLEMENTED / DOCUMENTED / TESTED / PLANNED / INFERRED / UNKNOWN
Relevant files:
Open questions:
```

5. Write the smallest accurate update. Preserve headings, style, and file organization unless changing them is part of the request.
6. Link technical claims to source, tests, requirements, planning tasks, commands, or existing docs when practical.
7. Mark stale, conflicting, planned, inferred, or unknown information explicitly.
8. Report changed files, evidence checked, unresolved uncertainty, and any human decisions needed.

## Source Priority

For current behavior, prefer sources in this order:

1. Source code
2. Tests
3. Generated API or schema files
4. Configuration defaults
5. Examples that are run or maintained with the project
6. Recent documentation
7. Older documentation
8. Planning documents
9. Issues, comments, or discussion notes

For intended behavior, requirements, ADRs, accepted planning tasks, and explicit user decisions may outrank current code. Mark the distinction clearly.

Example:

```markdown
[IMPLEMENTED] The current timeout default is 10 seconds in `src/config/defaults.ts`.

[PLANNED] `.documentation/requirements/networking.md` says the default should become 30 seconds.
```

## Writing Rules

- Preserve existing style unless there is a clear reason to change it.
- Prefer concrete commands, paths, symbols, examples, expected outcomes, and links.
- Use present tense for current behavior and future tense only for planned behavior.
- Keep headings stable when possible.
- Remove or mark stale information instead of leaving contradictions.
- Avoid broad rewrites, unrelated reformatting, generic filler, unsupported claims, and marketing language.
- Avoid unsupported adjectives such as `simple`, `easy`, `robust`, `secure`, `fast`, `production-ready`, `fully tested`, or `comprehensive`.
- Do not claim tests pass unless they were run or verified from recorded evidence.
- Do not claim full coverage unless coverage evidence exists.
- Do not change code behavior during a documentation-only task unless explicitly asked.

## Document Type Guidance

For README updates, keep orientation concise: what the project is, current status, how to start, common workflows, project structure, development/testing commands, documentation map, and known limitations.

For `AGENTS.md`, include durable repository instructions only: authoritative docs, commands, workflow rules, safety boundaries, known pitfalls, and when to use deeper skills or docs. Keep it short and link elsewhere.

For reference docs, include exact behavior: stability, import path or command, signature, parameters, defaults, units, return values, errors, side effects, examples, related types, source, and tests.

For explanations, distinguish current implementation from intended design. Explain rationale, tradeoffs, alternatives, limitations, and related decisions without turning the page into a tutorial.

For ADRs, document significant decisions that affect public APIs, data formats, deployment, dependencies, architecture, or hard-to-reverse tradeoffs. Do not rewrite historical ADRs to match the present; add a superseding ADR.

For troubleshooting, write from observable symptoms. Include exact error messages, likely causes, checks, fixes, and known uncertainty.

For examples, keep them minimal, correct, focused on one concept, and runnable when possible. Include expected output only when verified.

## Checklist

Before finishing, check:

```text
[ ] Relevant source, tests, existing docs, and applicable AGENTS.md files were read.
[ ] The audience and documentation type are clear.
[ ] Implemented, documented, tested, planned, inferred, unknown, and conflicting claims are separated.
[ ] The smallest useful set of files changed.
[ ] Existing structure and style were preserved where practical.
[ ] Technical claims link to evidence when practical.
[ ] Stale information was removed or marked.
[ ] Broad documentation churn and generic filler were avoided.
[ ] Limitations, open questions, and human decisions are visible.
```

## Final Response

After documentation work, report:

- Files created or changed and the purpose of each change.
- Important evidence checked.
- Uncertainties, stale or conflicting information, and `[TODO-HUMAN]` decisions.
- Validation commands or inspections performed.

If no files changed, explain why. If documentation could not be completed because evidence was missing, say what was missing and where you looked.
