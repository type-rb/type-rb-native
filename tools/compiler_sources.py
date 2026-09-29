#!/usr/bin/env python3
"""Compose compiler source roots without changing their logical module paths."""
import argparse
from pathlib import Path
import shutil


def source_files(root):
    root = Path(root)
    if not root.is_dir() or root.is_symlink():
        raise ValueError(f"expected a compiler source directory: {root}")
    sources = []
    for source in sorted(root.rglob('*')):
        if source.is_symlink():
            raise ValueError(f"compiler source symlink is not supported: {source}")
        if source.is_file() and source.suffix == '.trb' and not source.name.endswith('_test.trb'):
            sources.append((source.relative_to(root), source))
    return sources


def stage_sources(roots, destination):
    destination = Path(destination)
    selected = {}
    for root in roots:
        for relative, source in source_files(root):
            target = destination / relative
            if relative in selected or target.exists() or target.is_symlink():
                raise ValueError(f"compiler source collision: {relative}")
            for parent in target.parents:
                if parent.is_symlink() or parent.exists() and not parent.is_dir():
                    raise ValueError(f"invalid compiler source destination: {parent}")
                if parent == destination:
                    break
            selected[relative] = source
    # Validate every input and destination before publishing any staged file.
    for relative, source in selected.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
    return list(selected)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', type=Path)
    parser.add_argument('sources', type=Path, nargs='+')
    args = parser.parse_args()
    try:
        stage_sources(args.sources, args.destination)
    except (OSError, ValueError) as error:
        parser.exit(1, f"compiler source staging: {error}\n")


if __name__ == '__main__':
    main()
