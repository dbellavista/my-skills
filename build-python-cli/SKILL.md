---
name: build-python-cli
description: "Build or extend typed Cyclopts CLIs with lazy command registration, searchable metadata, structured output, Loguru logging, and testable application logic. Use for product command-line interfaces, not repository automation tasks."
---

# Build a Python CLI

Use a lightweight registry and typed plain functions. Keep product commands in an
application member and development automation in Invoke. Read
[the CLI design](references/cli-design.md) before adding commands.

## Scaffold or adapt

For a workspace made by `bootstrap-python-workspace`, run:

```bash
python3 /path/to/build-python-cli/scripts/add_cli.py /path/to/project --command examplectl
```

The script infers the namespace and distribution prefix from the ownership ledger,
creates an application member, updates workspace sources and ownership, and writes CLI
documentation. It installs nothing and refuses collisions before changing files.
Sync with `uv sync --all-packages` afterward. The script supports the companion
bootstrap layout; inspect and adapt assets instead for other layouts or existing CLIs.
The design is reusable independently and does not require that skill to be installed.

## Add a command

1. Put application logic in its owning library; keep the CLI function a thin adapter.
2. Write a typed `def` or `async def` under `commands/<group>/`. Prefer one or two
   positional identity arguments and keyword-only configuration. Use `Path`, enums,
   `Literal`, and repeatable lists rather than manually parsing strings.
3. Add a `CommandSpec` with its tuple path, `module:function` target, one-line help,
   and search tags. Keep help equal to the function's first docstring line. Use a
   NumPy-style `Parameters` section for argument help. Create nested group apps from
   metadata; do not import leaf modules while registering commands.
4. Return a JSON-serializable result, or `None`. The CLI boundary owns output and error
   status. Log stable messages with named kwargs using Loguru, never print diagnostics
   to stdout. Applications configure the shared formatter once.
5. For destructive operations, call the shared confirmation helper before mutation.
   Describe scope, support `--dry-run` when feasible, and require explicit `--yes` when
   stdin is not a terminal. A dry-run must perform no mutation and must report its plan.
6. Update the generated catalog, affected docs, and tests. Record actionable findings
   in the project's development backlog when appropriate.

## Verify

```bash
uv run examplectl --help
uv run examplectl find greeting
uv run examplectl --json greet Ada
uv run examplectl system ping
uv run examplectl catalog --output docs/cli.md
uv run inv check
uv run inv test.run --project apps/example-cli
```

Substitute the selected executable and distribution prefix. Test successful execution,
invalid inputs, expected failures, structured output, async execution, and destructive
confirmation behavior. Guard tests should resolve every target, validate registry names
and summaries, verify catalog freshness, and prove root/group help and search do not
import leaf modules. Build and install the wheel with its member dependencies before
claiming packaging works.

Shell completion is optional: consult the installed Cyclopts version, generate scripts
explicitly, and keep completion free of expensive startup or unbounded external lookups.
