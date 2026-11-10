"""Behavioral checks for the portable renderers and installer (standard library only)."""

import hashlib
import importlib.util
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP = ROOT / "bootstrap-python-workspace/scripts/bootstrap.py"
ADD_CLI = ROOT / "build-python-cli/scripts/add_cli.py"
INSTALL = ROOT / "scripts/install.py"


def run(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


def snapshot(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in root.rglob("*")
        if path.is_file()
    }


class BundleTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.project = self.base / "project with spaces"

    def bootstrap(self):
        result = run(
            BOOTSTRAP,
            str(self.project),
            "--name",
            "sample-project",
            "--namespace",
            "sample_ns",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_names_namespace_packaging_and_dependencies(self):
        self.bootstrap()
        for path in self.project.rglob("*.toml"):
            tomllib.loads(path.read_text())
        package = self.project / "packages/sample-project-core"
        manifest = tomllib.loads((package / "pyproject.toml").read_text())
        self.assertEqual(
            manifest["tool"]["uv"]["build-backend"]["module-name"], "sample_ns.core"
        )
        self.assertFalse((package / "src/sample_ns/__init__.py").exists())
        self.assertTrue((package / "src/sample_ns/core/__init__.py").exists())
        self.assertTrue((package / "src/sample_ns/core/py.typed").exists())
        for path in self.project.rglob("*.py"):
            compile(path.read_text(), str(path), "exec")
        self.assertEqual(len(list(self.project.rglob("uv.lock"))), 0)
        self.assertFalse((self.project / ".venv").exists())

    def test_bootstrap_refuses_existing_content(self):
        self.project.mkdir()
        (self.project / "keep.txt").write_text("preserve this")
        before = snapshot(self.project)
        result = run(
            BOOTSTRAP, str(self.project), "--name", "sample", "--namespace", "sample"
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.project), before)

    def test_invalid_names_write_nothing(self):
        for name, namespace in [
            ("bad/name", "valid"),
            ("good", "class"),
            ("good", "bad.name"),
        ]:
            result = run(
                BOOTSTRAP, str(self.project), "--name", name, "--namespace", namespace
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(self.project.exists())

    def test_cli_updates_workspace_and_catalog(self):
        self.bootstrap()
        result = run(ADD_CLI, str(self.project), "--command", "samplectl")
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = tomllib.loads(
            (self.project / "apps/sample-project-cli/pyproject.toml").read_text()
        )
        self.assertEqual(
            manifest["project"]["scripts"], {"samplectl": "sample_ns.cli.app:main"}
        )
        root_manifest = tomllib.loads((self.project / "pyproject.toml").read_text())
        self.assertTrue(
            root_manifest["tool"]["uv"]["sources"]["sample-project-cli"]["workspace"]
        )
        ledger = tomllib.loads(
            (self.project / "docs/workspace-ledger.toml").read_text()
        )
        self.assertEqual(ledger["members"][-1]["module"], "sample_ns.cli")
        self.assertTrue((self.project / "docs/cli.md").is_file())
        for path in self.project.rglob("*.py"):
            compile(path.read_text(), str(path), "exec")

    def test_cli_collision_leaves_every_file_unchanged(self):
        self.bootstrap()
        (self.project / "docs/cli.md").write_text("Existing catalog")
        before = snapshot(self.project)
        result = run(ADD_CLI, str(self.project), "--command", "samplectl")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.project), before)

    def test_cli_repeat_does_not_mutate(self):
        self.bootstrap()
        self.assertEqual(
            run(ADD_CLI, str(self.project), "--command", "samplectl").returncode, 0
        )
        before = snapshot(self.project)
        result = run(ADD_CLI, str(self.project), "--command", "otherctl")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.project), before)

    def test_installer_dry_run_copies_nothing(self):
        self.project.mkdir()
        result = run(
            INSTALL,
            "--agent",
            "codex",
            "--scope",
            "project",
            "--project",
            str(self.project),
            "--dry-run",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_project_installation_and_collision(self):
        self.project.mkdir()
        args = (
            "--scope",
            "project",
            "--project",
            str(self.project),
            "--skill",
            "evolve-python-workspace",
        )
        for agent, folder in [("codex", ".agents"), ("claude", ".claude")]:
            result = run(INSTALL, "--agent", agent, *args)
            self.assertEqual(result.returncode, 0, result.stderr)
            installed = self.project / folder / "skills/evolve-python-workspace"
            self.assertEqual(
                snapshot(installed), snapshot(ROOT / "evolve-python-workspace")
            )
        before = snapshot(self.project)
        result = run(INSTALL, "--agent", "antigravity", *args)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(snapshot(self.project), before)

    def test_global_destination_mapping_without_installing(self):
        spec = importlib.util.spec_from_file_location("bundle_installer", INSTALL)
        assert spec is not None and spec.loader is not None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        home = self.base / "fake-user"
        expected = {
            "codex": ".agents/skills",
            "claude": ".claude/skills",
            "antigravity": ".gemini/config/skills",
        }
        for agent, relative in expected.items():
            self.assertEqual(
                module.destination(agent, "global", None, home), home / relative
            )
        self.assertFalse(home.exists())


if __name__ == "__main__":
    unittest.main()
