"""Add a CLI to the companion bootstrap layout without overwriting existing files."""

import argparse
import re
import runpy
import tomllib
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--command", required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", args.command):
        parser.error("--command must be lowercase kebab-case")
    root = args.project.expanduser().resolve()
    try:
        ledger_path = root / "docs/workspace-ledger.toml"
        ledger_text = ledger_path.read_text()
        ledger = tomllib.loads(ledger_text)
        namespace = ledger["namespace"]
        core = next(
            item for item in ledger["members"] if item["module"] == namespace + ".core"
        )
        name = core["distribution"].removesuffix("-core")
        project_path = root / "pyproject.toml"
        project_text = project_path.read_text()
        project = tomllib.loads(project_text)
        python = (root / ".python-version").read_text().strip()
    except (OSError, KeyError, StopIteration, tomllib.TOMLDecodeError) as error:
        parser.error(f"Not a companion bootstrap workspace: {error}")
    if (
        not re.fullmatch(r"[a-z][a-z0-9_]*", namespace)
        or not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", name)
        or not re.fullmatch(r"3\.\d+", python)
    ):
        parser.error(
            "Workspace names or Python version are not supported by this renderer"
        )
    distribution = name + "-cli"
    if "[tool.uv.sources]" not in project_text:
        parser.error("Expected an explicit [tool.uv.sources] table")
    if distribution in project["tool"]["uv"].get("sources", {}) or any(
        item["distribution"] == distribution or item["module"] == namespace + ".cli"
        for item in ledger["members"]
    ):
        parser.error("CLI is already registered; adapt the existing member")
    if "apps/*" not in project["tool"]["uv"]["workspace"]["members"]:
        parser.error("Expected apps/* in workspace members")
    replacements = {
        "__NAME__": name,
        "__NAMESPACE__": namespace,
        "__COMMAND__": args.command,
        "__PYTHON__": python,
    }

    def render(text: str) -> str:
        for key, value in replacements.items():
            text = text.replace(key, value)
        return text

    assets = Path(__file__).resolve().parents[1] / "assets" / "cli"
    files = {
        root / render(str(source.relative_to(assets)))[:-5]: render(source.read_text())
        for source in assets.rglob("*.tmpl")
    }
    if not files:
        parser.error("Bundled CLI assets are missing")
    catalog = root / "docs/cli.md"
    if (
        (root / "apps" / distribution).exists()
        or catalog.exists()
        or any(target.exists() for target in files)
    ):
        parser.error(
            "CLI destination or documentation already exists; nothing was changed"
        )
    registry_target = (
        root / "apps" / distribution / "src" / namespace / "cli/registry.py"
    )
    # Execute only the trusted bundled registry text, never project code.
    import tempfile

    with tempfile.TemporaryDirectory() as temporary:
        registry = Path(temporary) / "registry.py"
        registry.write_text(files[registry_target])
        metadata = runpy.run_path(str(registry))
        files[catalog] = metadata["render_catalog"]()
    updated_project = project_text.replace(
        "[tool.uv.sources]",
        f"[tool.uv.sources]\n{distribution} = {{ workspace = true }}",
        1,
    )
    updated_ledger = ledger_text.rstrip() + render(
        '\n\n[[members]]\npath = "apps/__NAME__-cli"\n'
        'distribution = "__NAME__-cli"\nmodule = "__NAMESPACE__.cli"\n'
        'allows = ["__NAME__-core", "__NAME__-services"]\n'
    )
    tomllib.loads(updated_project)
    tomllib.loads(updated_ledger)
    for target, content in files.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x") as stream:
            stream.write(content)
    project_path.write_text(updated_project)
    ledger_path.write_text(updated_ledger)
    readme = root / "README.md"
    with readme.open("a") as stream:
        stream.write(
            "\nSee [CLI development](docs/cli-development.md) and [commands](docs/cli.md).\n"
        )
    print(
        f"Created {distribution}; run uv sync --all-packages, then uv run {args.command} --help"
    )


if __name__ == "__main__":
    main()
