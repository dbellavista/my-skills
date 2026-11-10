# CLI design

Example application layout:

```text
src/example/cli/
  __main__.py       python -m support
  app.py            root/meta app and output/error boundary
  registry.py       immutable command metadata and catalog renderer
  confirm.py        destructive-operation confirmation
  commands/         leaf functions, imported only when selected
```

Distribution names, import namespaces, and executable names are distinct. A console
script points to `example.cli.app:main`. The root app registers import strings using
Cyclopts, which supports lazy commands natively. Group apps are assembled from command
paths. For a large extension ecosystem, add explicit entry-point discovery only when
needed; a static registry is easier to inspect for a small application.

Metadata powers root/group help, `find`, and the Markdown catalog without importing
commands. Leaf help may load that leaf's module. Keep package `__init__.py` files light
and do not re-export all command functions. Add a subprocess test that inspects loaded
modules after listing and search, including group help.

The meta app owns global options (`--json`, `--log-level`), shared Loguru configuration,
and rendering. It delegates execution to Cyclopts so sync and async commands share one
boundary; commands never call `asyncio.run()` themselves. The starter supports global
options before the command; test any additional placement guarantees before documenting
them. Log level and result format are separate: JSON results go to stdout and JSON logs
to stderr. Results must retain JSON-native types; do not silently stringify arbitrary
return objects. If accepting models, serialize them explicitly at the boundary.

Expected domain errors produce concise stderr diagnostics and status 1. Parsing errors
use the framework's nonzero status. Unexpected errors retain tracebacks in logs; do not
catch exceptions and accidentally return success. Define additional exit codes only
when consumers need them.

A reusable confirmation helper must refuse unattended destructive execution without
`--yes`. Validate targets and determine scope first, report a dry-run plan without
mutation, and confirm before the first side effect. A `danger` command group is a useful
convention for irreversible maintenance actions, not a substitute for these safeguards.

The starter includes a greeting command and an async local health command as executable
examples. It deliberately does not include a real deletion command. Add confirmations
and tests when introducing one. Shared parameter aliases can be extracted as commands
grow; avoid building a framework before repetition exists.

Sources:

- [Cyclopts lazy loading](https://cyclopts.readthedocs.io/en/latest/lazy_loading.html)
- [Meta apps](https://cyclopts.readthedocs.io/en/latest/meta_app.html)
- [Result handling](https://cyclopts.readthedocs.io/en/latest/app_calling.html)
- [Loguru API](https://loguru.readthedocs.io/en/latest/api/logger.html)
