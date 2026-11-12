---
name: plan-and-run-experiments
description: "Design, execute, and review reproducible experiments with explicit model routing, defined terminology, frozen protocols, and evidence-backed decisions. Use for experiment planning, comparisons, and substantive result reviews."
---

# Plan and run experiments

Use this workflow for scientific or engineering experiments, including benchmarks,
ablations, and dataset or model comparisons. Scale the records to the question; a small
comparison can fit in one document. Planning does not authorize execution, spending,
provider calls, or changes to external systems. Preserve existing authorization and
project-specific operational rules. Do not impose software branch or commit checkpoints
on experiments unless the project or user requires them.

## Establish the question and records

Read applicable project instructions, relevant prior results, available artifacts, and
resource constraints. State the question, hypothesis, alternatives, intended decision,
and what evidence would change that decision. Separate confirmed facts from assumptions.
Reuse the project's experiment records and identifiers; otherwise use a concise experiment
document based on [the experiment template](references/experiment-template.md).

Maintain a protocol, terminology glossary, execution record, results, and decision in
those existing records. Preserve historical evidence. Definitions and procedures have one
canonical home; other documents link to them. Read-only analysis can proceed with the
available evidence while missing inputs are recorded explicitly.

## Require a glossary

Every experiment code, condition label, dataset/split alias, model alias, abbreviation,
acronym, metric shorthand, and mathematical symbol used in maintained experiment records
must have an explicit definition before first use. This includes labels in tables,
charts, legends, filenames, and handoffs. Ordinary words, programming syntax, and routine
library identifiers do not require entries unless repurposed as experiment terminology.

- Give each term its full name, operational meaning, and scope. A label such as `E1`
  needs the experiment's purpose and condition, not merely the expansion "experiment 1".
- Map aliases to exact dataset versions, split definitions, model/checkpoint identifiers,
  configuration versions, or artifact references when applicable. Distinguish a local
  alias from a provider or system identifier; do not invent missing identifiers.
- Define metrics and symbols with units, scale, aggregation, and preferred direction
  where applicable. Explain denominators and decision thresholds rather than relying on
  a familiar-looking name. Define the unit of observation separately from the unit of
  replication when they differ.
- Define terms at their canonical home and link or expand them at first use in a
  standalone report. Check captions, headings, tables, and exported artifacts as well
  as prose. Include a definition or glossary link in a report's available format.
- Keep codes stable within their scope and never silently reuse one for a different
  condition. Resolve conflicting definitions before comparing affected results. Mark
  unknown definitions as unresolved; do not guess their meaning or accept conclusions
  that depend on them. Audit inherited records before relying on their codes; annotate
  gaps without rewriting frozen historical records.

The glossary is required even for a small experiment; a short inline definition list is
sufficient. Terminology completeness is part of protocol and final-review acceptance.

## Route work by phase

Resolve exact available model identifiers from the runtime or user-supplied roster;
record planned and actual assignments. Provider names are not capability rankings.

1. **Evidence collection:** assign bounded artifact queries, schema inspection, baseline
   retrieval, and mechanical glossary audits to an economical suitable model. Require
   source references, uncertainties, and missing inputs.
2. **Protocol design:** use a strong reasoning model for hypotheses, comparison design,
   confounders, interpretation criteria, and resource tradeoffs.
3. **Execution:** use economical suitable models for bounded implementation, validation,
   authorized dispatch, and monitoring. Each task needs inputs, dependencies, owned
   artifacts, limits, expected outputs, checks, and escalation conditions.
4. **Review and interpretation:** use a strong review-capable model to assess protocol
   adherence, terminology, evidence quality, uncertainty, and the resulting decision.
   Prefer an independent context for a consequential review when available.

Use supported delegation or switching only within authorization. If routing is unavailable,
disclose that limitation, keep phases explicit, and record a handoff without claiming
another model performed the work. Never call a provider API merely to simulate routing.
Review does not add a human approval gate to already-authorized work.

## Specify and review the protocol

Before dispatch, record baselines and interventions; comparison conditions and controlled
variables; dataset provenance, versions and splits; leakage controls; exclusions; metrics;
replication/seeds and uncertainty analysis; resource budget; stopping and cancellation
rules; and acceptance/decision criteria. Explain paired versus unpaired comparisons and
the independent replication unit when relevant. Mark inapplicable fields with a reason.

Separate exploratory analysis from confirmatory claims. For confirmatory work, define
primary outcomes, thresholds, and relevant multiple-comparison handling before observing
outcomes. Choose sample size or precision goals appropriate to the decision; do not treat
many correlated samples as independent replications. Record remaining limitations.

Review the protocol and glossary before execution. Version the accepted protocol so later
changes remain visible. Do not silently change hypotheses, conditions, metrics, exclusions,
or budgets. Escalate changes that affect the intended comparison; document amendments
and whether existing runs remain comparable. Keep exploratory follow-ups distinct.

## Execute, interpret, and close

Dispatch only authorized work. Record run/job identifiers, protocol/configuration versions,
code revision when applicable, data/model versions, seeds, environment, artifact locations,
resource use, status, and deviations as work proceeds. Check constraints before dispatch
and during long runs. Stop at defined limits; report failures and partial results without
quietly rerunning until a favorable outcome appears.

Review results against the original hypothesis and protocol, including failed and excluded
runs, uncertainty, confounders, and glossary completeness. Distinguish observations from
causal claims and generalization. Record accept/revise/stop/inconclusive with its evidence
and consequences. An inconclusive result is valid; propose a bounded next experiment
rather than extending the budget implicitly. Assign concrete review findings as bounded
corrections and re-review affected conclusions. Preserve the original evidence.

Finish with the question, protocol version, model assignments and routing limits, results,
verification coverage, deviations, decision, unresolved terminology, and next action.
Update the project's existing experiment index, decision log, and follow-ups as applicable.
