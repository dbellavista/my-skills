"""Render the bundled workspace using only the Python standard library."""

import argparse
import keyword
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--name", required=True, help="Distribution prefix, kebab-case")
    parser.add_argument("--namespace", required=True, help="One Python identifier")
    parser.add_argument(
        "--python", default="3.12", help="Minimum and pinned minor version"
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", args.name):
        parser.error("--name must be lowercase kebab-case")
    if not re.fullmatch(r"[a-z][a-z0-9_]*", args.namespace) or keyword.iskeyword(
        args.namespace
    ):
        parser.error("--namespace must be a lowercase Python identifier, not a keyword")
    match = re.fullmatch(r"3\.(\d+)", args.python)
    if not match or int(match[1]) < 12:
        parser.error("--python must be a Python 3 minor version >=3.12")
    destination = args.destination.expanduser().resolve()
    if destination.exists() and (
        not destination.is_dir() or any(destination.iterdir())
    ):
        parser.error(
            "Destination must be new or empty; existing files are never overwritten"
        )
    replacements = {
        "__NAME__": args.name,
        "__NAMESPACE__": args.namespace,
        "__PYTHON__": args.python,
        "__RUFF_PYTHON__": "py" + args.python.replace(".", ""),
    }

    def render(text: str) -> str:
        for key, value in replacements.items():
            text = text.replace(key, value)
        return text

    assets = Path(__file__).resolve().parents[1] / "assets" / "workspace"
    files = {
        destination / render(str(source.relative_to(assets)))[:-5]: render(
            source.read_text()
        )
        for source in assets.rglob("*.tmpl")
    }
    if not files:
        parser.error("Bundled workspace assets are missing")
    for target, content in files.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("x") as stream:
            stream.write(content)
    print(f"Created {len(files)} files in {destination}")
    print("Next: uv sync --all-packages; uv run inv check; uv run inv test.all")


if __name__ == "__main__":
    main()
