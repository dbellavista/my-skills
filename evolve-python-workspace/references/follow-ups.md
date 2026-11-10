# Follow-up quality

Use the existing backlog format. For a new project, keep only unfinished work in
`docs/development/next-steps.md`. The backlog is an execution aid, not a transcript.

Example:

```markdown
- [ ] Reject ambiguous configuration keys before starting an operation.
  - Problem: unknown keys are silently ignored, so a typo changes behavior unnoticed.
  - Evidence: the configuration loader accepts `timeuot` without a diagnostic.
  - Next action: validate keys and provide a useful error listing unknown names.
  - Completion: a misspelled key fails before side effects; documented valid keys work.
```

Capture observed bugs, missing safeguards, repeated manual work, and concrete design
constraints. Distinguish a reproducible issue from an unverified suspicion. An uncertain
issue can be an investigation task when its question and useful outcome are explicit.

Before adding an item, search for an existing one with the same underlying problem.
Merge new evidence into it. Avoid generic entries such as "improve tests" or "clean up
architecture". Do not turn personal taste into mandatory work.

Priority should follow user impact, frequency, or dependency order. Use exact file paths
and symbols when helpful; avoid brittle line-number-only pointers. Do not invent an
owner, deadline, estimate, or user approval. A future task is not permission to execute it.

When completed, remove the item from the open list. Add delivered behavior to the
changelog or existing history system. Preserve important decision rationale in an
architecture decision record when needed; do not copy the full item everywhere.

For a task with no new findings, leave the backlog unchanged and report that only if it
helps explain closeout. Do not add a dated "nothing found" entry for every session.
