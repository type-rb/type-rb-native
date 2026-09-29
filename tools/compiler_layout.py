#!/usr/bin/env python3
"""Check compiler ownership boundaries, including tests and CLI composition.

These are responsibility rules, not a directory DAG. Reciprocal frontend/MIR
imports and mutually recursive checking modules are intentional.
"""
import argparse
from pathlib import Path
import re
import sys

GROUPS = {
    'support': {'support'},
    'state': {'state', 'support', 'frontend/types', 'mir'},
    'frontend/types': {'frontend/types', 'frontend/resolution', 'state', 'support'},
    'frontend/syntax': {'frontend/syntax', 'frontend/types', 'frontend/resolution', 'state', 'support'},
    'frontend/resolution': {'frontend/resolution', 'frontend/types', 'frontend/syntax', 'state', 'support', 'mir', 'project'},
    'frontend/checking': {'frontend/checking', 'frontend/types', 'frontend/resolution', 'frontend/syntax', 'state', 'support', 'mir', 'project'},
    'mir': {'mir', 'frontend/checking', 'frontend/types', 'frontend/syntax', 'frontend/resolution', 'state', 'support'},
    'backend/qbe': {'backend/qbe', 'mir', 'state', 'support', 'frontend/types'},
    'project': {'project', 'support', 'frontend/syntax', 'state'},
}
# Existing declaration-bound intrinsic identity and the shared parsed/checked
# iteration projection have narrow exceptions, not permission for whole layers.
EXCEPTIONS = {
    ('backend/qbe/qbe_constants', 'frontend/resolution/entry_resolution'),
    ('frontend/types/transform_model', 'frontend/syntax/iteration_syntax'),
    ('frontend/types/transform_model', 'mir/iteration_mir'),
}
IMPORT = re.compile(r'import (?:\{[^}]*\} from )?([a-z][a-z0-9_/]*)(?: as [A-Za-z_][A-Za-z0-9_]*)?(?:\s*#.*)?')


def import_header(source):
    """Return leading imports without interpreting embedded program fixtures."""
    result = []
    for number, line in enumerate(source.splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        if not line.startswith('import '):
            break
        match = IMPORT.fullmatch(line)
        if not match:
            raise ValueError(f'unsupported import header on line {number}: {line}')
        result.append((number, match.group(1)))
    return result


def check(root):
    root = Path(root)
    modules = {}
    errors = []
    for area in ('src', 'cli'):
        directory = root / 'compiler' / area
        for path in sorted(directory.rglob('*.trb')):
            relative = path.relative_to(directory)
            name = relative.with_suffix('').as_posix()
            label = path.relative_to(root).as_posix()
            if path.is_symlink() or not path.resolve().is_relative_to(directory.resolve()):
                errors.append(f'{label}: source must stay inside its declared root')
                continue
            if name in modules:
                errors.append(f'{label}: duplicate composed module {name}')
                continue
            group = 'cli' if area == 'cli' else relative.parent.as_posix()
            if group == '.' and (name == 'compiler' or name.endswith('_test')):
                group = 'entry'
            if group not in GROUPS and group not in ('entry', 'cli'):
                errors.append(f'{label}: missing responsibility owner')
            modules[name] = (path, group, name.endswith('_test'), area)
    if 'compiler' not in modules:
        errors.append('compiler/src/compiler.trb: missing compiler entry')
    edge_count = 0
    for name, (path, group, test, area) in modules.items():
        label = path.relative_to(root).as_posix()
        try:
            imports = import_header(path.read_text())
        except ValueError as error:
            errors.append(f'{label}: {error}')
            continue
        for line, target in imports:
            if target.startswith('trb/'):
                if target == 'trb/std/test' and not test:
                    errors.append(f'{label}:{line}: production code imports test support')
                continue
            edge_count += 1
            if target not in modules:
                errors.append(f'{label}:{line}: missing composed module {target}')
                continue
            _, target_group, target_test, target_area = modules[target]
            if area == 'src' and target_area == 'cli':
                errors.append(f'{label}:{line}: core cannot depend on CLI module {target}')
            elif not test and target_test:
                errors.append(f'{label}:{line}: production code imports test module {target}')
            elif test or group in ('entry', 'cli'):
                continue
            elif target_group not in GROUPS.get(group, set()) and (name, target) not in EXCEPTIONS:
                errors.append(f'{label}:{line}: forbidden responsibility dependency {group} -> {target_group} ({target})')
    return errors, len(modules), edge_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    errors, modules, edges = check(args.root)
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print(f'Compiler ownership: {modules} modules, {edges} explicit imports; directory cycles allowed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
