"""Update committed skill snapshots in a project from a Git revision."""

import argparse
import datetime
import hashlib
import io
import json
import subprocess
import tarfile
import tempfile
import tomllib
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def files(root):
    if root.is_symlink() or not root.is_dir():
        raise ValueError(f"Expected a regular directory: {root}")
    result = {}
    for path in root.rglob('*'):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not supported: {path}")
        if path.is_file():
            result[path.relative_to(root).as_posix()] = digest(path)
        elif not path.is_dir():
            raise ValueError(f"Unsupported file: {path}")
    return result


def quote(value):
    return json.dumps(value, ensure_ascii=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--agent', choices=['codex', 'claude'], default='codex')
    parser.add_argument('--skill', action='append', help='Select skills to add or update; defaults to existing imports')
    parser.add_argument('--revision', default='HEAD', help='Committed source revision (default: HEAD)')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--adopt-identical', action='store_true', help='Adopt existing copies only when identical to the selected revision')
    args = parser.parse_args()
    try:
        project = args.project.resolve(strict=True)
        if not project.is_dir():
            raise ValueError('Project must be a directory')
        target = project / ('.claude' if args.agent == 'claude' else '.agents') / 'skills'
        for parent in (target.parent, target):
            if parent.is_symlink():
                raise ValueError(f'Symlink destination is not supported: {parent}')
        manifest = target / 'imported-skills.toml'
        if manifest.is_symlink():
            raise ValueError('Manifest must not be a symlink')
        data = tomllib.loads(manifest.read_text()) if manifest.exists() else {}
        imports = data.get('imports', [])
        existing = {item['name']: item for item in imports}
        if len(existing) != len(imports):
            raise ValueError('Duplicate imports in manifest')
        selected = list(dict.fromkeys(args.skill or existing))
        if not selected:
            raise ValueError('Specify at least one --skill for a new manifest')
        for name in [*existing, *selected]:
            if not isinstance(name, str) or not name or name in ('.', '..') or '/' in name or '\\' in name:
                raise ValueError(f'Invalid skill name: {name!r}')
        revision = subprocess.check_output(['git', '-C', str(SOURCE), 'rev-parse', '--verify', args.revision + '^{commit}'], text=True).strip()
        archive = subprocess.check_output(['git', '-C', str(SOURCE), 'archive', revision])
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
                for member in tar.getmembers():
                    p = Path(member.name)
                    if p.is_absolute() or '..' in p.parts or not (member.isfile() or member.isdir()):
                        raise ValueError(f'Unsupported archive entry: {member.name}')
                tar.extractall(root)
            license_name = data.get('license_path', 'my-skills.LICENSE')
            if not isinstance(license_name, str) or Path(license_name).name != license_name or license_name in ('', '.', '..'):
                raise ValueError('Invalid license path')
            license_target = target / license_name
            if license_target.is_symlink():
                raise ValueError('License must not be a symlink')
            if license_target.exists() and (not data.get('license_sha256') or digest(license_target) != data['license_sha256']):
                raise ValueError(f'License has local changes: {license_target}')
            snapshots = {}
            for name in selected:
                source = root / name
                if not (source / 'SKILL.md').is_file():
                    raise ValueError(f'No skill at revision {revision}: {name}')
                snapshots[name] = files(source)
                dest = target / name
                if dest.exists() or dest.is_symlink():
                    if name not in existing:
                        if not args.adopt_identical or files(dest) != snapshots[name]:
                            raise ValueError(f'Untracked destination already exists or differs: {dest}')
                        continue
                    recorded = {entry['path']: entry['sha256'] for entry in existing[name].get('files', [])}
                    if files(dest) != recorded:
                        raise ValueError(f'Imported skill has local changes: {dest}')
                elif name in existing:
                    raise ValueError(f'Imported skill is missing: {dest}')
            print(f'Source revision: {revision}')
            for name in selected:
                print(f'{name} -> {target / name}')
            if args.dry_run:
                print('Dry run only')
                return
            import shutil
            target.mkdir(parents=True, exist_ok=True)
            for name in selected:
                dest = target / name
                if name not in existing and dest.exists():
                    pass  # An identical existing snapshot was explicitly adopted.
                else:
                    if dest.exists():
                        shutil.rmtree(dest)
                    shutil.copytree(root / name, dest)
                existing[name] = {'name': name, 'source_head': revision, 'imported_at': datetime.date.today().isoformat(), 'files': [{'path': p, 'sha256': h} for p, h in sorted(snapshots[name].items())]}
            shutil.copyfile(root / 'LICENSE', license_target)
            lines = ([f'source_path = {quote(data["source_path"])}'] if 'source_path' in data else []) + [f'source_head = {quote(revision)}', f'license_path = {quote(license_name)}', f'license_sha256 = {quote(digest(license_target))}', '']
            for item in existing.values():
                lines += ['[[imports]]', f'name = {quote(item["name"])}']
                if 'source_head' in item:
                    lines.append(f'source_head = {quote(item["source_head"])}')
                if 'imported_at' in item:
                    lines.append(f'imported_at = {quote(str(item["imported_at"]))}')
                for entry in item.get('files', []):
                    lines += ['', '[[imports.files]]', f'path = {quote(entry["path"])}', f'sha256 = {quote(entry["sha256"])}']
                lines.append('')
            manifest.write_text('\n'.join(lines))
            print('Updated snapshots and manifest; review and commit the project diff.')
    except (ValueError, OSError, KeyError, tomllib.TOMLDecodeError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f'Error: {exc}\n')


if __name__ == '__main__':
    main()
