# Reusable development skills

Six portable agent skills for development, experiments, and Python workspaces. This directory
is a source bundle: keeping it here installs nothing and changes no agent settings.

| Skill | Use |
| --- | --- |
| [bootstrap-python-workspace](bootstrap-python-workspace/SKILL.md) | Create a uv workspace with namespace packaging, Ruff, ty, pytest, Invoke, RTK, and Loguru. |
| [build-python-cli](build-python-cli/SKILL.md) | Build a typed Cyclopts CLI with lazy imports, search, and structured output. |
| [evolve-python-workspace](evolve-python-workspace/SKILL.md) | Maintain member boundaries, documentation, and actionable development follow-ups. |
| [dream-project-knowledge](dream-project-knowledge/SKILL.md) | Consolidate available conversations, memories, docs, and custom skills into durable guidance. |
| [plan-model-work](plan-model-work/SKILL.md) | Plan dependency-aware work packages, model assignments, commits, and reviewed milestones with explicit pause and branch choices. |
| [plan-and-run-experiments](plan-and-run-experiments/SKILL.md) | Design and review reproducible experiments with model routing, a mandatory glossary, versioned protocols, and bounded execution. |

## Install into a project or globally

Copy a complete skill directory, including references, scripts, and assets. `SKILL.md`
must sit directly inside that directory. The bundled installer uses Python >=3.10 and
only the standard library; it refuses existing destinations instead of overwriting them.

| Agent | Project directory | Global directory |
| --- | --- | --- |
| Codex | `<project>/.agents/skills/` | `~/.agents/skills/` |
| Claude Code | `<project>/.claude/skills/` | `~/.claude/skills/` |
| Antigravity App, CLI, IDE | `<project>/.agents/skills/` | `~/.gemini/config/skills/` |

Verified against official documentation on 2026-11-10:
[Codex](https://learn.chatgpt.com/docs/build-skills),
[Claude Code](https://code.claude.com/docs/en/skills), and
[Antigravity](https://antigravity.google/docs/skills).
These instructions cover local agent environments; remote/cloud sessions may need their
own installation. Antigravity also documents legacy IDE paths; use the shared current path above.

From this bundle directory, install all six for one project:

```bash
python3 scripts/install.py --agent codex --scope project --project /path/to/project --dry-run
python3 scripts/install.py --agent codex --scope project --project /path/to/project
python3 scripts/install.py --agent claude --scope project --project /path/to/project
```

Codex and Antigravity share the same project destination. One copy serves both; do not
run a second installation into that directory. Commit project skills to share them with
collaborators. To install just one, add `--skill evolve-python-workspace`; repeat `--skill`
to select several.

For global use, choose the agents you use:

```bash
python3 scripts/install.py --agent codex --scope global
python3 scripts/install.py --agent claude --scope global
python3 scripts/install.py --agent antigravity --scope global
```

Run these commands only when you want installation. No installer runs automatically.
Prefer one scope per agent to avoid same-named copies. For updates, compare the installed
directory with this source, preserve local customizations, then replace the chosen copy.
To uninstall, remove only the installed skill directory you selected.

Copies are portable snapshots. For Codex only, a documented alternative is a symlinked
skill folder; this keeps local updates synchronized but ties discovery to this bundle's
location. Use copies when committing skills for a team. Restart the agent or open a new
session if an installed skill does not appear.

## Invoke a skill

In Codex, use `$bootstrap-python-workspace`, `$build-python-cli`,
`$evolve-python-workspace`, `$dream-project-knowledge`, `$plan-model-work`, or
`$plan-and-run-experiments` in your prompt.
In Claude Code and Antigravity App/CLI, use `/` followed by the skill name. In the
Antigravity IDE, mention the skill by name and inspect the Customizations menu. You can also ask in
natural language; descriptions support automatic selection. Confirm the intended skill
appears in the agent's skill selector or customization view.

Example requests:

```text
Use bootstrap-python-workspace to create a Python workspace at /path/to/example
with distribution prefix example, import namespace example, and Python 3.12.

Use build-python-cli to add examplectl to that workspace.

Use evolve-python-workspace to add a reporting library, maintain dependency boundaries,
and record any actionable improvements discovered during the work.

Use dream-project-knowledge to review the available session context, project memories,
docs, and custom skills. Correct stale guidance, consolidate duplicates, preserve
decisions, and report unavailable sources and unresolved questions.

Use plan-model-work to plan a new feature. Assign each work package to an available
model, include dependencies and commit checkpoints, and use milestones where useful.
Ask me when to pause and which branch to use. Require strongest-model reviews and
assign any resulting fixes as new work packages.

Use plan-and-run-experiments to design a baseline-versus-intervention comparison.
Define every experiment code, dataset/model alias, abbreviation, and metric in a glossary.
Assign available models to protocol design, evidence collection, execution, and review.
Record leakage controls, uncertainty, resource limits, and stopping criteria before runs.
```

`plan-model-work` governs software implementation packages and commits.
`plan-and-run-experiments` governs empirical questions, protocols, runs, and interpretation;
it does not introduce mandatory branch choices or a commit per experiment. Use both when
an experiment requires substantial implementation, keeping each record in its existing home.

## Bootstrap before installing project skills

The bootstrap renderer expects a new or empty target. If you first install skills into
that target, it is no longer empty. Either install the bootstrap skill globally, ask the
agent to read its `SKILL.md` by absolute path without installing, or render first:

```bash
python3 bootstrap-python-workspace/scripts/bootstrap.py /path/to/example \
  --name example --namespace example --python 3.12
python3 build-python-cli/scripts/add_cli.py /path/to/example --command examplectl
python3 scripts/install.py --agent codex --scope project --project /path/to/example
```

Then run the generated workspace commands from its root:

```bash
uv sync --all-packages
uv run inv check
uv run inv test.all
uv run examplectl --json greet Ada
uv build --all-packages
```

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and
[RTK](https://github.com/rtk-ai/rtk) using upstream instructions. RTK is a separate binary,
not a Python package. Development tasks support `--no-rtk` for direct tool output.

## Agent continuity

The generated `AGENTS.md` makes follow-up tracking part of ordinary substantive work.
Current Codex and Antigravity read project `AGENTS.md` instructions. Claude Code can read
it directly when no project `CLAUDE.md` takes precedence; for compatibility, merge
`@AGENTS.md` into an existing `CLAUDE.md` when needed instead of replacing its content.
See [Claude instruction loading](https://code.claude.com/docs/en/memory) and
[Antigravity rules](https://antigravity.google/docs/rules) for version-specific details.

`evolve-python-workspace` tracks improvements to implement. `dream-project-knowledge`
improves the guidance used to implement them. Dreaming is on demand; scheduling and
access to additional history or memories are separate configuration decisions.

## Publishing and customization

All examples use neutral names and no private services. Tool constraints are compatible
ranges; each generated project commits its resolved lockfile. Review Python and tool
versions when adopting the template. Choose a license before publishing your own copy.
Scripts never initialize Git, install dependencies, register skills, or publish anything
implicitly. No license choice is imposed on generated projects.

## Validate changes to this bundle

Create the local validation environment with uv (Python >=3.12):

```bash
uv sync --locked
uv run --locked python -m unittest discover -s tests -v
```

The development dependency group includes PyYAML for the skill-creator validator.
When that skill is installed, run its validator using this environment, for example:

```bash
uv run --locked python /path/to/skill-creator/scripts/quick_validate.py plan-model-work
```

Use the actual path of your installed skill-creator. The validator is supplied by that
skill; it is not bundled here. Commit `uv.lock` to keep the validation environment
reproducible. The installer and bundle tests still use only the Python standard library.

The nine tests exercise rendering, independent names, namespace layout, collision refusal,
and installation behavior without changing actual global agent directories. For changes to
assets, also generate a disposable project and run its checks, tests, builds, and clean-wheel
installation. See [validation results](VALIDATION.md) for the performed checks and limits.
