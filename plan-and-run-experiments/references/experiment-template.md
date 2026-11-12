# Experiment record template

Adapt this to existing project records. Replace illustrative codes with locally meaningful
ones, define them before use, and leave unknowns explicitly unresolved. One document is
sufficient for a small experiment; link to canonical records rather than duplicating them.

## Question and decision

- Question, hypothesis, and plausible alternatives:
- Decision this experiment informs:
- Evidence that would support, reject, or leave the hypothesis unresolved:
- Scope, prior evidence, assumptions, and limitations:
- Mode and authorization: planning / read-only analysis / authorized execution; limits:

## Glossary and identifiers

Every code and shorthand used below needs a definition here or a link to its canonical
definition. The following entries illustrate the required specificity; they are not a
prescribed naming system or an actual experiment.

| Term | Full name and operational meaning | Scope / exact artifact or definition |
| --- | --- | --- |
| E1 | Experiment comparing baseline predictions with predictions after a fixed image resize | This record; link to accepted protocol and run records |
| C0 | Baseline condition: original images, no resize | E1; exact input dataset version and preprocessing configuration |
| C1 | Intervention condition: resize each input's longest side to 512 pixels, preserving aspect ratio | E1; specify interpolation and all remaining preprocessing |
| D0 | Evaluation dataset shared by both conditions | Immutable dataset version, split manifest, exclusions, and provenance |
| M0 | Frozen model used for both conditions | Exact model/checkpoint ID and runtime configuration |
| accuracy | Fraction of correct predictions, range 0–1; higher is better | Define labels, denominator, weighting, and aggregation |
| delta_accuracy | Accuracy for C1 minus accuracy for C0; range −1–1 | Paired comparison on the same eligible samples; positive favors C1 |

Expand other acronyms and define additional metrics and symbols before use. Artifact
aliases remain unresolved until their actual versions or identifiers are recorded. State
the independent replication unit; paired samples alone do not establish independence.

## Model assignments and bounded tasks

Record exact available identifiers and actual execution separately from intended routing.

| Phase / task | Inputs and dependencies | Model and reason | Output / owned artifacts | Checks, limits, and escalation |
| --- | --- | --- | --- | --- |
| Evidence collection | | | | |
| Protocol design | | | | |
| Execution and monitoring | | | | |
| Protocol and result review | | | | |

- Routing tools, delegation authorization, and unavailable capabilities:
- Handoff when intended routing cannot be performed:

## Protocol

- Version, status, date, and review outcome:
- Baseline, intervention, controlled variables, confounders:
- Dataset provenance, exact versions, split construction, leakage controls, exclusions:
- Model/checkpoint and configuration versions:
- Unit of observation, independent replication unit, seeds, pairing, and sample size:
- Metrics, aggregation, uncertainty method, primary outcomes, and decision thresholds:
- Exploratory versus confirmatory scope; multiple-comparison handling if applicable:
- Resource budget, allowed concurrency, monitoring, stopping/cancellation criteria:
- Acceptance criteria and outcomes that require escalation:
- Relevant inapplicable fields and reasons:

Review the glossary and protocol before dispatch. Record amendments below; do not overwrite
the protocol that produced existing results.

## Execution and evidence

| Run / job identifier | Protocol and code revision | Data / model / configuration versions | Seed / environment | Status / resources | Artifacts / deviations |
| --- | --- | --- | --- | --- | --- |

- Failed or excluded runs and reasons:
- Amendments, dates, rationale, and comparability impact:
- Verification actually performed and unavailable checks:

## Results, review, and decision

- Observations and uncertainty, linked to artifacts:
- Comparison against the original hypothesis and acceptance criteria:
- Protocol deviations, confounders, and limits on causal or general claims:
- Glossary audit: undefined/ambiguous codes, aliases, acronyms, symbols, and captions:
- Review model actually used, scope, findings, corrections, and re-review:
- Decision: accept / revise / stop / inconclusive; evidence and consequences:
- Unresolved questions and bounded next action, with resource implications:

Update existing indexes and decision records. Preserve historical run evidence and frozen
records; a correction should identify what it changes and why.
