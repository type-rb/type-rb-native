#!/usr/bin/env python3
"""Synchronize recovery import boundaries with canonical compiler sources."""

import argparse
import json
import re
from pathlib import Path


ENTRY = re.compile(
    r'(?m)^\t\tRecoveryCompilerModule\.new\(name: "([^"]+)", imports: ("(?:\\.|[^"\\])*")\),$'
)


def canonical_imports(source: Path) -> str:
    lines = source.read_text().splitlines(keepends=True)
    count = 0
    while count < len(lines) and lines[count].startswith("import "):
        count += 1
    if count == 0:
        return ""
    if count < len(lines) and lines[count] == "\n":
        count += 1
    return "".join(lines[:count])


def synchronize(root: Path, write: bool) -> list[str]:
    layout = root / "src/compiler_recovery_layout.trb"
    original = layout.read_text()
    names: set[str] = set()
    changed: list[str] = []

    def replace(match: re.Match[str]) -> str:
        name, encoded = match.group(1), match.group(2)
        if name in names:
            raise ValueError(f"duplicate recovery module {name}")
        names.add(name)
        source = root / "compiler/src" / f"{name}.trb"
        if not source.is_file():
            raise ValueError(f"missing canonical compiler module {name}")
        expected = json.dumps(canonical_imports(source), ensure_ascii=False)
        if encoded == expected:
            return match.group(0)
        changed.append(name)
        return match.group(0).replace(encoded, expected) if write else match.group(0)

    updated = ENTRY.sub(replace, original)
    if not names or len(names) != original.count("RecoveryCompilerModule.new(name:"):
        raise ValueError("recovery layout contains an unrecognized module row")
    if write and updated != original:
        layout.write_text(updated)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    changed = synchronize(root, args.write)
    if changed:
        print("Recovery import boundaries differ: " + ", ".join(changed))
        if args.check:
            print("Run python3 tools/recovery_layout_sync.py --write")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
