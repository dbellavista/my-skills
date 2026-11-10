# Review method

## Make an evidence map

For each candidate lesson, identify the claim, source, date when known, scope, current
verification, and intended destination. This can be working notes; do not create a new
permanent database merely to run a review. Preserve links to supplied artifacts when
useful. If a source has no stable link, cite its filename or a concise session identifier.

Useful evidence includes an explicit user decision, a repeated correction, a reproducible
failure, and current code demonstrating the actual behavior. An agent's previous confident
statement is not proof. Distinguish a statement about current behavior from a user request
to change it. A later observation can show implementation drift without superseding intent.

Suggested review order:

1. Current user request and applicable instruction files.
2. Relevant manifests, executable workflows, and current docs.
3. Available conversations and durable project memories.
4. Relevant custom skills and their references, scripts, and assets.

Expand only where findings point. In a large project, choose an explicit module, time
range, or workflow and state coverage. Do not claim a whole-history audit after reading
only the visible conversation.

## Decide the disposition

| Finding | Useful response |
| --- | --- |
| Confirmed stale instruction | Correct it and retain a compatibility note if needed. |
| Duplicate procedure | Keep one maintained source and replace copies with useful links. |
| Conflicting user decisions | Use the latest explicit decision when scope matches; flag ambiguity. |
| Repeated narrow workaround | Document its conditions; verify whether the cause still exists. |
| Unverified suspected bug | Record a concrete investigation task if the impact warrants it. |
| Missing unavailable memory | Report the gap and limit conclusions. |
| Skill with broad activation | Narrow the description to its actual capability and triggers. |
| Rare but important exception | Preserve it concisely; frequency is not the only measure of value. |

Measure improvement through reduced contradiction, easier discovery, and successful
execution of relevant examples. Shorter text alone is not evidence of a better result.

## Validate behavior

For changed skill guidance, consider realistic requests it should and should not handle.
Check routing and outcomes without embedding the expected answer in the request.
Automated or independent evaluation can help when authorized and available; it is not
required for every wording edit. Use isolated artifacts and no live external side effects.

Example bounded request: "Review the supplied two session summaries and the CLI docs;
consolidate repeated command-registration guidance and record any unresolved findings."
A useful outcome corrects the relevant sources, preserves decision rationale, and reports
which history was unavailable. It does not silently change global preferences.
