---
name: evolve-python-workspace
description: "Evolve a Python workspace: add or move members, maintain ownership and dependency boundaries, and close substantive development tasks by updating docs and recording actionable follow-ups. Use during architectural changes, development closeout, or commit preparation; follow Conventional Commits when committing."
---

# Evolve a Python workspace

Keep the repository understandable as it grows, and preserve useful findings for the
next agent. Apply architecture guidance when structure changes; apply closeout guidance
after substantive development. Skip redundant bookkeeping for trivial edits.

## Establish the current contract

Read applicable project instructions, the root and affected member manifests, ownership
documentation, and the existing development backlog. Inspect the working tree to avoid
including unrelated changes. Reuse established conventions and task names. The paths
below are defaults for a new project, not reasons to reorganize an existing one.

## Evolve architecture

Read [member evolution](references/member-evolution.md) when adding, splitting, or moving
code. Maintain explicit ownership, an acyclic dependency graph, member-owned runtime
dependencies, stable public imports, and correct namespace packaging. Update the ledger
and lockfile when relevant. Add no placeholder members merely to imitate a larger system.

## Close substantive work

Before declaring completion:

1. Verify the changed behavior with focused tests and relevant lint/type/packaging checks.
   Report actual results and any coverage limitations. Do not claim unrun checks passed.
2. Update docs affected by observable behavior, commands, configuration, or architecture.
   Update an existing reusable skill when its procedure changed; do not duplicate it.
3. Review findings discovered during this task. Resolve findings needed for the current
   goal. Record useful out-of-scope improvements in `docs/development/next-steps.md`.
4. Remove completed backlog items. Add a concise changelog entry for meaningful delivered
   behavior, using the project's existing format. Record implementation history there
   rather than leaving completed items in the open-work list.

Read [follow-up quality](references/follow-ups.md) when creating or consolidating items.
A good item names the concrete problem, evidence, next action, and completion criteria.
Include affected paths, dependencies, and priority only when they improve execution.
Deduplicate first. No findings is a valid outcome; do not invent work to satisfy a ritual.

## Commit conventions

When a commit is part of the task, follow
[Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/):

```text
type(scope): concise summary
```

Use `feat` for new functionality and `fix` for bug fixes. Other useful types are `docs`,
`refactor`, `perf`, `test`, `build`, `ci`, `style`, and `chore`; follow the project's chosen
vocabulary. The scope is optional and identifies the affected member or capability. Prefer
a short imperative summary describing the resulting change. Reserve `style` for formatting
changes that do not change behavior.

Mark breaking changes with `!` before the colon or a `BREAKING CHANGE:` footer. Explain
the compatibility impact and migration in the message. Add a body when rationale or
tradeoffs help; separate the subject, body, and footers with blank lines.

```text
feat(cli): add command search
fix(config): reject unknown keys
docs(workspace): explain member ownership
refactor(core)!: rename the public configuration loader
```

Keep each commit cohesive and review the staged diff before writing its message. Match
the type, scope, and summary to the actual changes. Mention only verification that ran.
For squash workflows, apply the convention to the final squash commit message as well.

## Keep the responsibility discoverable

In a new project, add this short convention to its agent instruction file; in an existing
project, merge it with equivalent guidance instead of repeating it:

> After substantive work, update affected docs and record actionable, evidence-backed
> follow-ups in the development backlog. Deduplicate existing items, remove completed
> work, and record meaningful delivered changes in the changelog. Do not invent follow-ups.

An installed skill is not guaranteed to load in every session. This short repository
instruction keeps the responsibility visible without requiring every agent to read the
full skill. If accumulated guidance needs consolidation, use `dream-project-knowledge`
when available; this skill works without it.

Finish with what changed, relevant verification, and any remaining concrete follow-ups.
Do not expand the current implementation to complete the entire backlog.
