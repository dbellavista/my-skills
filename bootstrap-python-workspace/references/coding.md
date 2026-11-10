# Python coding conventions

Use typed function boundaries, concrete domain types, small cohesive modules, and
dependencies owned by the member importing them. Use `TYPE_CHECKING` for imports needed
only by annotations. Keep package initialization lightweight. Ruff owns linting, import
sorting, and formatting; ty owns type checking. Avoid parallel formatter stacks.

## Logging

Loguru is the primary logging API:

```python
from loguru import logger

logger.info("Import completed", source=str(source), records=count)
scoped_logger = logger.bind(operation_id=operation_id)
scoped_logger.debug("Input validated", input_path=str(path))
```

Prefer a stable event message and named context fields over f-strings or preformatted
messages. Direct kwargs are captured in `record["extra"]`. Use `bind()` for reusable
context and `contextualize()` for scoped context, including concurrent async operations.
Avoid expensive computations merely to construct disabled debug entries.

Configure logging once at an application entry point with the shared
`<namespace>.core.logging.configure_logging`. Library imports never add or remove sinks.
Applications own level and format settings. Keep CLI results on stdout and logs on stderr.
Do not log secrets or raw credentials. Exceptions should retain their traceback and be
logged at the boundary that handles them; avoid repeated logging at each layer.

The provided custom callable formatter renders time, level, source, stable message,
and structured fields. A callable returns a format template, not an already formatted
line; include newline and exception placeholders explicitly. Field values containing
braces must remain values, never become format-string syntax. The template has tests
for that distinction. JSON mode uses Loguru serialization and preserves the `extra`
dictionary. `diagnose=False` avoids including local variable values in tracebacks.

[Loguru API](https://loguru.readthedocs.io/en/latest/api/logger.html)

## Development commands

```bash
uv run inv check
uv run inv format
uv run inv test.run --project packages/example-core
uv run inv test.all
uv run inv check --no-rtk
```

`check` never fixes files. `format` applies Ruff formatting and import sorting; lint
violations still require review. Root tooling uses `uv run rtk <tool>` where supported.
Use the direct command via `--no-rtk` for complete raw diagnostics. RTK is a separate
executable: follow [upstream instructions](https://github.com/rtk-ai/rtk) and verify
installed-version support instead of assuming every command has a wrapper.
