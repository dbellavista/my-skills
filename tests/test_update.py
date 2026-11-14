import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('updater', Path(__file__).resolve().parents[1] / 'scripts/update.py')
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class UpdateTests(unittest.TestCase):
    def test_install_update_and_local_change_refusal(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source, project = root / 'source', root / 'project'
            source.mkdir()
            project.mkdir()
            subprocess.run(['git', 'init', '-q', str(source)], check=True)
            subprocess.run(['git', '-C', str(source), 'config', 'user.email', 'test@example.com'], check=True)
            subprocess.run(['git', '-C', str(source), 'config', 'user.name', 'Test'], check=True)
            (source / 'LICENSE').write_text('license')
            (source / 'example').mkdir()
            (source / 'example/SKILL.md').write_text('first')
            def commit():
                subprocess.run(['git', '-C', str(source), 'add', '.'], check=True)
                subprocess.run(['git', '-C', str(source), 'commit', '-qm', 'change'], check=True)
            def run(*args):
                with patch.object(updater, 'SOURCE', source), patch('sys.argv', ['update', '--project', str(project), *args]):
                    updater.main()
            commit()
            run('--skill', 'example', '--dry-run')
            self.assertFalse((project / '.agents').exists())
            run('--skill', 'example')
            dest = project / '.agents/skills/example/SKILL.md'
            (source / 'example/SKILL.md').write_text('second')
            commit()
            run()
            self.assertEqual(dest.read_text(), 'second')
            dest.write_text('local')
            with self.assertRaises(SystemExit):
                run()
            self.assertEqual(dest.read_text(), 'local')


if __name__ == '__main__':
    unittest.main()
