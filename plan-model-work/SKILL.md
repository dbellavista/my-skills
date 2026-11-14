---
name: plan-model-work
description: "Plan development work as dependency-aware work packages with model assignments, durable recovery checkpoints, bounded coordination, and strongest-model reviews. Use when creating or revising an implementation plan and its execution workflow, including subscription quota constraints; scale structure to the task."
---

# Plan work across models

Produce an executable plan that balances quality, model cost, and coordination overhead.
Planning alone does not start implementation, launch agents, or authorize Git mutations.
When execution is requested, carry the plan's dependencies, review gates, commits, and
user-selected pause policy through execution.

Treat sessions as replaceable: repository artifacts and a compact execution record must
carry progress across quota exhaustion or session loss. Model assignments do not require
a different model or a separate agent for every WP; reuse a suitable executor when that
reduces startup and context costs.

## Establish the execution contract

Inspect applicable project instructions, relevant code and tests, the current branch,
working-tree changes, and existing planning conventions. Resolve architectural choices
that materially affect scope, interfaces, compatibility, or verification. Record useful
assumptions instead of asking about routine implementation details.

Before finalizing the plan, ask for these choices unless already answered in the session:

- **Pause policy:** after every work package, after every reviewed milestone, only for
  problems or decisions requiring user input, or a custom checkpoint policy. Recommend
  milestone pauses for substantial work and problems-only pauses for small, clear tasks.
- **Branch policy:** use the current branch (name it), or another branch. For another
  branch, clarify whether to use an existing branch or create one; propose a name and base.

Ask these together with unresolved architecture questions where practical. Continue
independent investigation while answers are pending. Do not treat silence as a branch
choice or permission to cross a requested pause. Honor choices already given without
asking again. A plan can remain provisional while these required answers are pending.

Determine which exact model identifiers and agent-routing tools are available. Use runtime
capabilities, project configuration, or the user's model roster. If unavailable, ask for
the roster and use explicitly provisional assignments until it is known. Distinguish
planned assignments from models that can actually be launched in this environment.

Record the funding mode (subscription, API, or unknown), shared quota pools, telemetry
availability, concurrency, and coordinator budget. Infer these from available evidence;
ask only when a missing choice materially affects execution or cost. Never silently
enable paid overages or change billing mode. For subscription execution, quota uncertainty,
or costly coordination, read [quota and recovery guidance](references/quota-and-recovery.md).

## Choose the useful amount of structure

Every plan has at least one work package (WP). Split when work has separate acceptance
criteria, different model needs, a meaningful dependency, or a useful commit boundary.
Keep packages cohesive and independently verifiable; avoid tiny packages created merely
to increase parallelism. An investigative WP may deliver a decision or findings document.

Use milestones only when they provide meaningful integration, risk, or user checkpoints:
for example, settling a public interface before implementing its consumers, or validating
a migration before switching traffic. Several WPs do not automatically need milestones.
For a small task, use one or a few WPs followed by one final review gate.

For every WP, specify:

- Stable ID, outcome, scope or owned files/interfaces, and acceptance criteria.
- Dependencies by WP ID, or explicitly `none`; include required review gates.
- One exact executor model and a short reason for the assignment.
- Relevant verification and a cohesive commit boundary or proposed commit subject.
- Milestone membership when milestones are useful.
- Durable checkpoint location and a bounded next step when interruption recovery matters.

Dependencies must form an acyclic graph. Identify the critical path and parallel-ready
packages only when useful. Consumers depend on a reviewed milestone when their work
requires its accepted contract. Parallel WPs need disjoint ownership or an explicit
integration strategy; coordinate commits so agents do not stage each other's changes.

## Assign models by the work

Choose the least costly available model likely to complete the WP reliably, considering
ambiguity, reasoning depth, context size, tool support, and the cost of correcting errors.
Provider names are examples of user-supplied rosters, not a permanent capability ranking.
Do not assume an alias exists or silently replace an assigned model.

| Work | Assignment preference |
| --- | --- |
| Bounded mechanical changes with precise acceptance criteria | Available economical model, such as a user-designated Haiku, Luna, or Flash |
| Ordinary implementation and focused tests | Available implementation model, such as a user-designated Sonnet or Terra |
| Ambiguous architecture, subtle concurrency, difficult debugging, or high-impact migration | Strongest suitable reasoning model |
| Milestone and final code review | Strongest available review-capable model in the chosen roster |

Record the actual model for each role. Names such as Opus, Sol, Argon, or Argus are not
interchangeable identifiers: resolve the intended model from the available roster. Ask
only if ambiguity affects a real assignment. Escalate a WP when investigation reveals
greater complexity or an unsuccessful attempt shows the assignment is inadequate;
update the plan and explain the reason. Do not repeatedly spend cheap attempts on a
problem needing stronger reasoning. Request a decision if the needed model is unavailable
or a change exceeds the user's cost constraints.

Include quota headroom and restart cost in routing decisions. Multiple agents or models
may consume the same subscription pool; parallelism improves latency, not the allowance.
Default to one active executor per shared pool when headroom is unknown. Increase only
with evidence and within the execution contract. Preserve the assigned review gate when
quota is low; defer it instead of silently weakening it.

## Bound coordination and preserve progress

Keep the coordinator focused on ready-package selection, dispatch, result validation,
integration, and review gates. Give workers only their WP contract, relevant paths, and
accepted dependency artifacts. Request compact completion records with evidence links;
avoid importing full transcripts or repeating worker investigation and verification.

Use completion/blocker notifications or runtime waits when available. Do not spend model
turns repeatedly polling unchanged agents. With no event mechanism, use bounded status
checks and back off, or record a handoff for the next explicit activation; do not promise
automatic resumption. Batch independent dispatch and bookkeeping decisions.

Set a concrete per-activation coordinator budget and say how it is enforced. Prefer a
runtime-enforced token/turn/cost cap when supported, leaving checkpoint headroom. Otherwise
use a soft default of at most three scheduling decisions per activation (dispatch a ready
batch, handle a result batch, or advance a gate), then persist state and wait or hand off.
Do not count progress narration as useful scheduling. This bounds activity, not exact
tokens; include input, output, reasoning, and repeated context in any measured token budget.
Keep review/implementation budgets separate and state whether runtime accounting includes
children. Exhausting a budget requires a recovery checkpoint, not a completion claim.

Each worker writes a compact checkpoint after a meaningful verified substep and before
expensive operations, handoffs, or context loss. Keep one owned record per active WP and
one coordinator-owned execution index. Record partial edits and failed or unrun checks;
an interrupted WP remains incomplete until its acceptance checks and commit succeed.
Checkpoint writes within a WP do not require additional Git commits.

On quota pressure, stop new dispatch into the affected pool and checkpoint in-flight work
where possible. A hard cutoff may prevent a final write, so never rely on a shutdown
summary alone. On resumption, reconcile saved state against Git and actual artifacts,
check whether old workers still run, and continue the next incomplete step without
replaying the conversation. Follow the reference for quota observations, drain thresholds,
and recovery fields. Quota/budget handoffs supplement the chosen pause policy; they never
waive a requested user pause or authorize extra spending.

## Gate delivery on review and fixes

Each milestone requires code review by the strongest available review-capable model.
Plans without milestones require the same review at the end. Prefer a fresh reviewer
context, even when the reviewer uses the same model as the implementer. Review the
integrated change against the base commit and acceptance criteria, including dependency
boundaries, regressions, and relevant verification evidence.

The reviewer returns findings with severity, affected locations, evidence or reproduction,
and a concrete completion criterion. A clean review is valid; do not manufacture fixes.
Turn every actionable in-scope finding into a fix WP with its own ID, dependencies,
executor model, verification, and commit boundary. Link it to the finding and review gate.
Record out-of-scope suggestions separately; do not quietly expand the task to implement them.

Fix WPs inherit the same execution, pause, verification, and commit rules as original WPs.
Re-review their combined result with the strongest review model, including regressions
introduced by fixes. A milestone closes only when its acceptance criteria pass and its
required findings are resolved. Any user-authorized deferral must be recorded with its
remaining risk; unresolved blockers keep the gate open.

Plan `implement -> verify -> commit -> review -> fix WPs -> verify/commit -> re-review`.
Do not pre-invent fix packages before findings exist. If the same blocker survives two
fix-and-review cycles without meaningful progress, pause with the evidence and a proposed
change of approach. This is a problem pause even under problems-only execution.

## Commit and pause semantics during execution

On execution, establish the chosen branch before implementation and record its base
commit. Preserve unrelated working-tree changes. A branch-switch conflict requires a
decision; do not automatically stash, discard, or transplant user changes.

Each completed WP, including every fix WP, gets a separate cohesive commit after its
acceptance checks pass. Follow project commit conventions, stage only that WP's changes,
and record the commit hash and actual verification in the plan. A documentation or
investigation WP commits its durable deliverable. Do not create empty commits or mark a
WP complete without its required artifact and commit; revise an unnecessary package or
record a blocked commit instead. Do not amend or squash package commits unless requested.

Keep `implemented/committed` distinct from `reviewed/accepted`. At a per-WP pause, stop
after verification and commit, before starting another WP or review; name the next action.
At a per-milestone pause, complete review, fix packages, and re-review before handing
control back. Without milestones, the final review is that checkpoint. Problems-only
execution continues through ordinary fix packages within scope.

A requested pause is a real handoff: report completed IDs, commits, verification,
findings, and the next ready action, then wait for the user to resume. In parallel
execution, drain in-flight work to safe checkpoints and launch nothing beyond the pause.
All policies still pause for blocking decisions, unavailable required models, or scope
changes requiring user input. Progress updates alone are not pauses.

## Deliver and maintain the plan

Use the project's planning location and format; otherwise use a concise Markdown plan.
Use [the plan template](references/plan-template.md) as a starting point and omit optional
sections that add no value. Record scope, execution contract, model roster, WPs,
dependencies, review gates, and acceptance criteria. Do not promise actual parallel
execution or model switching when the environment cannot perform it; identify handoffs.

Check that every WP has a model, dependencies, verification, and commit boundary; every
milestone has a strongest-model review; and review findings can feed assigned fix WPs
back through the gate. Record unanswered required choices as pending. During authorized
execution, keep status, findings, checks, and commit hashes current so another session
can resume without reconstructing the conversation. Include quota observations or explicit
unknowns, coordinator budget/enforcement, and recovery pointers when applicable. A planning
document specifies these controls; it does not itself install monitoring, enforce caps,
or arrange scheduled restarts.
