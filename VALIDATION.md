# Validation

## Planning quota and recovery update — 2026-11-14

- Added shared-pool quota admission, bounded coordinator activity, per-WP recovery
  records, and restart reconciliation to `plan-model-work` and its plan template.
- Checked provider guidance against official Codex app-server, Claude Code status-line
  and CLI, and Antigravity quota documentation. Inspected local Codex CLI 0.169.0 help;
  no total-run token-budget flag was exposed there. No live account quota was queried.
- The updated skill passed the skill-creator structural validator; all nine bundle
  tests passed using the existing validation environment. Local skill reference links
  and `git diff --check` passed.
- No monitors, runtime caps, scheduled restarts, or global skill installations were
  configured. No live quota exhaustion or autonomous-agent recovery test is claimed.

## Experiment workflow addition — 2026-11-12

- Added `plan-and-run-experiments` with a mandatory terminology glossary, experiment
  protocol template, model routing, bounded execution, and evidence-based review.
- All nine standard-library bundle tests passed in a temporary copy of the bundle.
- The new skill passed the skill-creator structural validator using the existing bundle
  validation environment. Local Markdown reference links passed direct checks.
- A selected-skill dry run changed nothing; an installation into a temporary project
  copied the skill and reference byte-for-byte. A repeated installation refused the
  collision and preserved all installed files. No global installation was performed.
- One independent model exercise used undefined experiment aliases, unversioned artifacts,
  correlated video-derived samples, and a two-GPU-hour cap. It kept unresolved terms
  explicit, proposed protocol and routing requirements, and dispatched no jobs. This
  limited behavioral check does not validate scientific outcomes or live execution.

## Planning skill addition — 2026-11-12

- All nine standard-library bundle tests passed after adding `plan-model-work` to the
  installer roster.
- Direct checks passed for the new skill's name, required frontmatter fields, local
  reference link, absence of unfinished scaffold markers, and installer roster coverage.
- A selected-skill dry run passed. An actual installation into a temporary project
  copied the skill and reference byte-for-byte; no global installation was performed.
- Added a uv validation environment with Python 3.12.11 and PyYAML 6.0.3, declared in
  the development dependency group and resolved in `uv.lock`.
- All five skills passed the standard skill-creator structural validator using that
  environment. All nine bundle tests also passed under `uv run --locked`.
- `git diff --check` passed. No autonomous agent behavioral evaluation is claimed.

## Original bundle validation — 2026-11-10

Validated on 2026-11-10 with Python 3.12, uv 0.13.7, RTK 1.1.0, Ruff 0.17.4,
ty 0.0.99, pytest 9.2.0, Invoke 2.2.1, Cyclopts 5.4.0, and Loguru 0.7.3.

- All four `SKILL.md` files passed the skill-creator structural validator.
- Nine standard-library bundle tests passed: rendering, independent names, namespace
  packaging, invalid inputs, collision refusal, dry-run installation, full skill copies,
  shared project destinations, and global destination mapping.
- A fresh project used different distribution and import names in a path containing spaces.
  Its checks passed without post-generation formatting: Ruff lint and formatting, ty for
  root tasks and each of three members, and workspace boundary validation.
- Sixteen generated tests passed in separate member processes: ten CLI tests, four core
  tests, and two services tests. Coverage includes async execution, JSON result/log stream
  separation, lazy help/search, target registration, catalog freshness, input failures,
  confirmation behavior, and formatter handling of braces and exceptions.
- Deliberately invalid namespace initialization, an undeclared internal import, and a
  dependency cycle were each rejected. Invalid task selection returned a nonzero status.
- All three members built both source distributions and wheels. Wheel contents retained
  namespace boundaries, included typing markers, and contained only each member's package.
- All three wheels installed together in a separate environment. Imports and sync/async CLI
  execution worked from outside the source checkout.
- Bundle Python scripts and tests passed Ruff and ty. Local Markdown links and neutral
  content were audited.

Installation paths and invocation instructions were checked against the linked official
documentation. Actual global installation and interactive discovery in the three agents
were not performed. No skills were registered. The evolution and dreaming skills received
editorial and structural review; no autonomous agent behavioral evaluation is claimed.
