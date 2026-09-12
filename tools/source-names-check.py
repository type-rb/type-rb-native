#!/usr/bin/env python3
"""Keep retired experiment-stage names out of active compiler/recovery code."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
IDENTIFIER = re.compile(r"(?<![A-Za-z0-9])_*(?:Gate[0-6]|GATE[0-6]_+|gate[0-6]|qbe[23]_|trbn_g[0-6])[A-Za-z0-9_]*\b")
PATH_NAME = re.compile(r"(?:gate[-_]?[0-6]|gate-zero|qbe[23])(?:[_.-]|$)", re.I)


def main():
    paths = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    errors = []
    for relative in paths:
        path = ROOT / relative
        if not relative or not path.is_file():
            continue
        parts = Path(relative).parts
        if parts[0] not in {"src", "compiler", "corpus", "fixtures", "tools", ".github"}:
            continue
        if path.suffix != ".md" and any(PATH_NAME.match(part) for part in parts):
            errors.append(f"{relative}: retired stage name in active path")
        if path.suffix != ".trb":
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            for match in IDENTIFIER.finditer(line):
                errors.append(f"{relative}:{number}: retired identifier {match.group()}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Active source names passed; no stage-name compatibility identifiers remain")
    return 0


if __name__ == "__main__":
    sys.exit(main())
