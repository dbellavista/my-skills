# Implementation plan template

Adapt this to the project's format. Remove optional milestone and parallelism sections
when they add no value. Replace angle-bracket fields with concrete values; leave unknown
choices explicitly pending rather than implying agreement.

## Outcome and scope

- Desired behavior and overall acceptance criteria: <observable result>
- Scope boundaries: <included work and relevant exclusions>
- Architectural decisions and assumptions: <decisions, rationale, pending questions>

## Execution contract

- Mode: <planning only / execution requested>
- Pause policy: <per WP / per reviewed milestone / problems only / custom; pending if unanswered>
- Branch policy: <current named branch / existing branch / new branch and base; pending if unanswered>
- Base commit: <record when execution starts>
- Model roster: <exact identifiers, capabilities, availability, relevant cost constraints>
- Review model: <strongest available review-capable model and identifier>
- Execution support: <available routing tools or required manual handoffs>
- Funding and quota pools: <subscription / API / unknown; account aliases, shared model groups>
- Quota observations: <source, timestamp, usage/reset per exposed window, or unknown>
- Admission policy: <concurrency per pool, reserve/drain threshold, unknown-headroom behavior>
- Coordinator budget: <per-activation token/turn/cost cap or soft scheduling-decision bound;
  enforcement mechanism, child accounting, checkpoint reserve, cumulative use if available>
- Recovery support: <execution index path, WP record location, completion notifications/wait
  support, supported reset wakeup or manual resume; no implied monitoring installation>

Keep quota/budget fields brief for small plans; explicit unknowns are valid. Use the
[quota and recovery guidance](quota-and-recovery.md) when these constraints matter.

## Work packages

| ID | Outcome and scope | Depends on | Executor model and reason | Acceptance and verification | Commit boundary | Milestone |
| --- | --- | --- | --- | --- | --- | --- |
| WP-01 | <cohesive outcome> | none | <exact model; reason> | <observable criteria and checks> | <proposed subject> | <optional> |
| WP-02 | <cohesive outcome> | WP-01 | <exact model; reason> | <observable criteria and checks> | <proposed subject> | <optional> |

## Milestones and review gates (optional)

| Milestone | Included WPs | Acceptance criteria | Review gate and model | Work blocked until accepted |
| --- | --- | --- | --- | --- |
| M1 | <IDs> | <integrated outcome> | <gate ID; exact strongest review model> | <IDs or none> |

For plans without milestones, specify one final review gate and its exact model.
If useful, record the critical path, parallel-ready WPs, file ownership, and integration
order. Include gate dependencies in the WP table, not only in prose.

## Review and fix ledger

Populate from actual reviews; an empty ledger is valid before execution or after a clean
review. Each fix WP also appears in the work-package table with all required fields.

| Finding | Gate / reviewed commits | Severity and evidence | Fix WP / executor model | Re-review result or authorized deferral |
| --- | --- | --- | --- | --- |

## Execution record and handoff

| WP | Status | Commit | Actual verification and result | Remaining blocker |
| --- | --- | --- | --- | --- |

Use statuses that distinguish pending, running, blocked, committed, and accepted.
For interruption-prone execution, link each active WP's compact checkpoint: timestamp,
owner/session, directory/branch/base, latest commit and partial artifacts, current substep,
actual checks, remaining checks, decisions, live jobs, blocker, and exact next action.
Update after meaningful substeps, not just completion; partial work remains incomplete.
The coordinator owns the shared index, while workers own their individual records.
Record quota/budget interruptions and relevant reset observations without implying a
scheduled restart. Reconcile records with Git and live workers before resuming.
At a requested pause, record the next ready action and wait for the user's resume.
At completion, record final review coverage and any explicitly deferred findings.
