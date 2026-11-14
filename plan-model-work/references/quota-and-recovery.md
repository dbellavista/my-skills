# Subscription-aware execution and recovery

Read when subscription limits, interruption recovery, or coordinator overhead affect
the execution plan. Use existing project records rather than building a new scheduler
unless the user requests one.

## Observe the right limit

Keep three measurements separate: session context occupancy, tokens consumed by a run,
and account/model quota remaining. A large context window or low output-token setting
does not establish subscription headroom. Quotas may be shared across tools, models,
agents, and unrelated sessions; a snapshot is not a reservation or a completion guarantee.

For each pool record the provider/account alias (no credentials), model group, funding
mode, observation source and timestamp, window usage/reset time when exposed, and any
known active consumers. Record missing windows as unknown, never zero usage. Recheck
before dispatch and after meaningful work or a quota notification; avoid a separate LLM
call solely to poll. Prefer native notifications or inexpensive local telemetry.

Client visibility is different from model visibility. If a supported local integration
already exists, it can pass a minimal quota snapshot to the scheduler or write a readable
file. A UI meter, status line, or protocol method is not automatically an agent tool.
Do not scrape credentials or rely on undocumented private endpoints to manufacture access.
If no supported signal reaches the agent, say so and use conservative bounded execution.

### Platform discovery pointers

Checked 2026-11-14. Verify installed version, authentication, and surface before using
these features; read only the relevant provider documentation when refreshing this table.
These are integration options, not monitors installed by this skill.

| Surface | Documented signal or control | Execution implication |
| --- | --- | --- |
| Codex | [App-server protocol](https://learn.chatgpt.com/docs/app-server): `account/rateLimits/read`, `account/rateLimits/updated`, and `thread/tokenUsage/updated`; quota windows expose usage percentages and reset timestamps. | A host integration can inspect quota and thread usage. These protocol methods are not shell commands or necessarily exposed tools in a chat. Use the actual window durations and bucket IDs returned. |
| Claude Code | [Status-line data](https://code.claude.com/docs/en/statusline): `rate_limits.five_hour` and `rate_limits.seven_day` supply `used_percentage` and `resets_at` for supported subscription sessions after a response; fields may be absent. The local status-line script consumes no API tokens. | An existing script can persist a minimal snapshot for an agent/scheduler. Displaying it alone does not inject it into model context; handle missing or expired windows as unknown. |
| Claude Code headless | [CLI reference](https://code.claude.com/docs/en/cli-reference): print mode supports `--max-turns` and `--max-budget-usd`. The latter checks estimated API spend, includes subagents, can overshoot, and does not carry earlier-run spend into a resumed run's cap. | Verify version and accounting. A USD estimate is not a subscription-quota cap; leave headroom, persist checkpoints, and track cumulative workflow use outside individual invocations when needed. |
| Antigravity (Agy) | [CLI model quotas](https://antigravity.google/docs/cli/commands/usage/): `/usage` (alias `/quota`) refreshes an interactive quota panel, including shared model-group limits. [Plans](https://antigravity.google/docs/plans) documents quota settings and overage controls. | Inspect the installed surface's supported facilities. A CLI panel or Settings view does not establish a callable quota API for an IDE agent. Without supported machine-readable access, use user-provided observations or mark headroom unknown. |

Do not infer a universal hard token cap from these features. Check the runtime's actual
options. For example, locally inspected `codex exec --help` in CLI 0.169.0 did not expose
a total-run token-budget flag. A host that observes usage can stop subsequent dispatch
or interrupt work, but observed usage can lag and an in-flight call can exceed a budget.
An output cap or reasoning-effort setting alone does not bound total workflow tokens.

## Admission and drain policy

Use user-specified thresholds when provided. Otherwise, start with one active executor
per shared subscription pool when headroom is unknown. A useful configurable starting
reserve is 15% in every applicable observed window: stop admitting new WPs at 85% used,
or earlier when the next bounded step plus verification and checkpointing is unlikely
to fit. This is a heuristic, not a provider guarantee; measured workload history can
justify a larger reserve. Reserve capacity for review and recovery as well as execution.

- Adequate observed headroom: admit bounded work within the concurrency contract.
- Low headroom: launch nothing new in the pool; ask running workers to reach their next
  safe checkpoint. Do not promise they can finish before cutoff.
- Exhausted pool: record the blocker and reported reset time, preserve partial work,
  and stop dispatch/retry loops. Distinguish a long quota exhaustion from a transient
  throttle; use only bounded, provider-guided retries for the latter.
- Unknown headroom: retain checkpoints and low concurrency; do not require telemetry
  merely to make progress or invent remaining-token estimates.

Switch providers or models only through an available, already authorized routing option;
otherwise record the proposed reassignment for a decision. A different model may share
the exhausted pool. Keep verification and strongest-model review requirements intact.
Do not keep an LLM active waiting hours for reset. Use an already supported host wakeup
or hand off with the earliest reported reset; re-observe all relevant windows on resume.
A short-window reset does not establish that the weekly limit has cleared.

## Keep coordination inexpensive

Separate planning, scheduling, implementation, and review roles without requiring a
separate session for each. One suitable executor may complete sequential WPs; use a
fresh reviewer context when practical. Do not create agents solely to fill roles.

Persist the dependency graph once and update changed rows. Workers return WP ID, status,
commit or partial-artifact paths, checks/results, blockers, and next step, normally within
200 words plus evidence links. The coordinator checks acceptance evidence and integration
risks; it does not reread every file or rerun every successful check without a reason.
Retain access to full evidence when a review or failure requires it.

Define coordinator activations around dispatch, result/blocker batches, and gate changes.
Use a cheap suitable coordinator with sufficient tool reliability when routing permits;
strong reasoning remains available for architectural decisions and required reviews.
Record a token/turn/cost cap if measurable and supported, or the skill's soft scheduling
decision bound otherwise. Measure total coordinator use across activations, including
context input and reasoning, when telemetry permits; concise replies alone do not prove
low consumption. Never label a prompt instruction as an enforced runtime limit.

## Minimal durable recovery record

The execution index points to the plan, branch/base, WP ownership and checkpoint paths,
active session/job IDs when available, latest pool observations, review gates, budget
use, and next ready action. Workers update only their own records; the coordinator
updates shared scheduling state. Keep records compact and replace stale detail.

Each active WP checkpoint contains:

- WP ID, assigned model, working directory/worktree, branch, base and latest commit.
- Current substep, intended result, changed files/artifacts, and uncommitted work.
- Checks actually run and their results, including failures; checks still required.
- Decisions and dependency artifacts needed to continue, with paths rather than transcripts.
- Exact next action, blockers, and any running command/job with duplicate-execution risk.
- Owner/session ID when available, timestamp, and status such as running, interrupted,
  quota-blocked, committed, or accepted. Keep committed distinct from reviewed/accepted.

Checkpoint after meaningful edits or checks, before expensive work, and at handoff.
Do not write on every tool call. Save partial work without claiming acceptance or making
an incomplete completion commit. A final report or a native session ID alone is insufficient
because the runtime can stop before producing it or session history may be unavailable.

On resume, read the execution index and only the ready WP's record, contract, and relevant
dependency artifacts. Verify Git status, commits, artifact availability, live worker/job
state, and current quota before redispatch. If an old worker's state is uncertain, resolve
ownership before launching another writer; quota failure does not prove all agents died.
Reconcile stale records against actual files and rerun interrupted or unverifiable checks.
Resume a native session when useful and supported, or start a replacement from the durable
record. Continue the first incomplete substep; do not rerun accepted WPs merely to rebuild
context. Honor branch rules and outstanding user pauses throughout recovery.
