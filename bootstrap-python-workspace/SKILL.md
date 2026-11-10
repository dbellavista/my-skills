---
name: bootstrap-python-workspace
description: "Bootstrap a Python-only uv workspace with PEP 420 namespace packages, Ruff, ty, pytest, Invoke, RTK, and structured Loguru logging. Use for a new structured Python repository; preserve existing architecture when adapting an established project."
---

# Bootstrap a Python workspace

Create a small working workspace that can grow through explicit member dependencies.
Read [architecture](references/architecture.md) for naming and ownership decisions and
[coding conventions](references/coding.md) before writing Python.

## Inputs and defaults

Infer names from the request when possible. Otherwise use a neutral example and state
the assumption. The renderer accepts a distribution prefix (`example`), one import
namespace (`example`), and a Python minor version (default `3.12`). These are independent
concepts; do not derive imports by blindly replacing distribution hyphens.

Use a single shared PEP 420 namespace. The renderer deliberately supports one namespace
identifier; adapt the assets for a requested nested namespace. Python >=3.12 is required.
Do not overwrite an existing repository with a scaffold. Inspect it and apply the
conventions selectively instead.

## Create

Locate this skill's directory using the path supplied by the agent, then run:

```bash
python3 /path/to/bootstrap-python-workspace/scripts/bootstrap.py /path/to/new-project \
  --name example --namespace example --python 3.12
```

The script uses only the standard library, writes into a new or empty directory, and
installs nothing. It renders the files in `assets/workspace/`: a virtual root, two
library members (`core`, `services`), development tasks, meaningful starter tests,
documentation, and agent instructions. The services member demonstrates a declared
dependency on core. Remove or rename the example functionality as the product takes shape.

## Complete and verify

From the generated root:

```bash
uv sync --all-packages
uv run inv check
uv run inv test.all
uv build --all-packages
```

Review the selected Python version and tool constraints; update them when needed and
commit the generated `uv.lock`. RTK is an external executable, not a Python dependency.
Install it using its upstream instructions if absent. The default tasks require RTK;
`--no-rtk` runs tools directly for diagnosis or environments without it. Do not install
unrelated packages named `rtk` from a Python index.

Build and install all member wheels together into a clean environment and verify
namespace imports outside the source checkout. This detects packaging errors editable
installs can hide. Also run `uv run inv -l` and check that failure exit codes propagate.

For a CLI, apply `build-python-cli` if available, or follow that skill's published
instructions explicitly. The workspace itself does not depend on another skill.
Preserve the generated closeout instructions: agents record evidence-backed follow-ups
in `docs/development/next-steps.md`, remove completed entries, and update documentation
and the changelog after substantive changes. Never manufacture follow-ups.

## Scope

Keep this Python-only. Add infrastructure, services, CI, publishing, or licenses only
when requested. Do not copy machine-specific paths or configuration into the result.
