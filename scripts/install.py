"""Copy selected skills into an agent discovery directory. No overwrite or registration API."""

import argparse
import shutil
from pathlib import Path

SKILLS = (
    "bootstrap-python-workspace",
    "build-python-cli",
    "evolve-python-workspace",
    "dream-project-knowledge",
    "plan-model-work",
    "plan-and-run-experiments",
)


def destination(agent: str, scope: str, project: Path | None, home: Path) -> Path:
    if scope == "project":
        if project is None:
            raise ValueError("--project is required for project scope")
        return project / (".claude" if agent == "claude" else ".agents") / "skills"
    return (
        home
        / {
            "codex": ".agents/skills",
            "claude": ".claude/skills",
            "antigravity": ".gemini/config/skills",
        }[agent]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent", choices=["codex", "claude", "antigravity"], required=True
    )
    parser.add_argument("--scope", choices=["project", "global"], required=True)
    parser.add_argument("--project", type=Path)
    parser.add_argument("--skill", action="append", choices=SKILLS)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.scope == "project" and args.project is None:
        parser.error("--project is required for project scope")
    if args.scope == "global" and args.project is not None:
        parser.error("--project is only valid for project scope")
    project = args.project.expanduser().resolve() if args.project is not None else None
    if project is not None and not project.is_dir():
        parser.error("Project directory must already exist")
    source = Path(__file__).resolve().parents[1]
    selected = tuple(dict.fromkeys(args.skill or SKILLS))
    target = destination(args.agent, args.scope, project, Path.home())
    for name in selected:
        if not (source / name / "SKILL.md").is_file():
            parser.error(f"Missing source skill: {name}")
        if (target / name).exists() or (target / name).is_symlink():
            parser.error(
                f"Destination exists; review it before updating: {target / name}"
            )
    for name in selected:
        print(f"{source / name} -> {target / name}")
        if not args.dry_run:
            target.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source / name, target / name)
    print(
        "Dry run only"
        if args.dry_run
        else "Copied skills; no other settings were changed"
    )


if __name__ == "__main__":
    main()
