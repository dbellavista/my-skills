# Architecture and naming

A uv workspace shares one lockfile and environment. Its root is virtual (`package = false`).
Each member has a `pyproject.toml`, `src/`, and `tests/`. Libraries go in `packages/`,
applications in `apps/`. Start with the smallest useful dependency graph.

- Distribution: `example-core` (normalized package name).
- Import: `example.core` (valid Python identifiers).
- Entry point: independently chosen, such as `examplectl`.

PEP 420 shared namespace directories omit `__init__.py`. An ordinary subpackage belongs
to one distribution and can contain `__init__.py`. Prefer explicit dotted `module-name`
values for `uv_build`; a new member must not package siblings owned by another member.
Declare `py.typed` per owned package when shipping typed code.

Runtime dependencies belong in the importing member. `tool.uv.sources` maps internal
distribution names to `{ workspace = true }`; the member must still declare the
dependency. Root development dependencies hold repository tooling. Every member needs a
compatible Python requirement because uv resolves the workspace together.

The starter's `docs/workspace-ledger.toml` records import ownership and allowed member
dependencies. Treat it as an architectural contract; `inv workspace.check` verifies
membership, observed internal imports, dependency declarations, and namespace boundaries.
Its AST check handles literal absolute imports and ordinary relative imports. Dynamic
imports require explicit review; this is a useful guard, not a complete dependency analyzer.

Keep dependency flow acyclic. Move shared contracts down the graph or inject behavior
rather than adding a circular dependency. Preserve public dotted imports when moving
code. If compatibility cannot be preserved, document the migration explicitly.

Run ty separately per member and for root tasks. Run pytest separately per member to
retain local configuration and avoid collisions among test module names. Shared fixtures
can later become a small testing member; do not import another member's `tests` package.

Sources:

- [uv workspaces](https://docs.astral.sh/uv/concepts/projects/workspaces/)
- [uv build backend](https://docs.astral.sh/uv/concepts/build-backend/)
- [PEP 420](https://peps.python.org/pep-0420/)
- [ty workspace guidance](https://docs.astral.sh/ty/reference/typing-faq/)
