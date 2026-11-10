# Member evolution

## Add a member

Choose its responsibility and imports before creating files. A library belongs under
`packages/`, an executable application under `apps/`, unless the repository already uses
another layout. A regular import package has one owning distribution.

Create a member manifest, `src/` package, and member-local tests. Match the workspace
Python requirement and build backend. For a shared PEP 420 namespace, omit `__init__.py`
at every split point and configure an explicit dotted module name where possible.
Check the built wheel contains its package and not a sibling's files.

Declare each runtime dependency in the importing member. Add internal dependencies to
the workspace source mapping. Update ownership and allowed dependency edges. A workspace
source mapping alone does not declare a dependency. Keep development tools at the root
unless a member has a specific development-only requirement.

Confirm task discovery picks up the member without a hardcoded list, sync all packages,
and regenerate the lockfile. Test the new member separately, run boundary checks and
per-member type checks, then build and test clean wheel installation.

## Move or split code

Identify consumers: ordinary imports, entry points, dynamic import strings, serialized
references, and docs. Move files between members while retaining the public dotted
module path when possible. Verify no regular package in one member hides a namespace
portion in another. A split inside a formerly regular package needs deliberate handling.

Move tests with their owner and put shared test helpers in a dedicated reusable package
only when needed. Never import another member's test tree. Update dependency declarations
on both sides and remove now-unused dependencies.

Resolve forbidden upward imports by moving shared contracts down, injecting dependencies,
or introducing a small interface. Do not silence the boundary check merely to make a
cycle pass. If a public import must change, document the migration and provide a shim
where practical.

## Verification

In the companion scaffold, run `uv run inv workspace.check`, focused member tests,
`uv run inv check`, and `uv build --all-packages`. Install all related wheels together
outside the checkout and test imports and executable entry points. If the project has
additional manifests for packaging or deployment, update those when applicable.
