#!/usr/bin/env python3
"""Keep retired experiment-stage names out of active compiler/recovery code."""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
# Removed with the verified successor seed handoff tracked by issue #412.
# The published predecessor dispatches these six intrinsics by source name.
SEED_BRIDGE = {
    "gate4_file_exists", "gate4_read_source", "gate4_source_slice",
    "gate4_collect_project_sources", "gate4_eputs", "gate4_reset_temporary_storage",
}
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
                if relative == "compiler/src/compiler.trb" and match.group() in SEED_BRIDGE:
                    continue
                errors.append(f"{relative}:{number}: retired identifier {match.group()}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Active source names passed; six registered predecessor-seed intrinsics remain")
    return 0


if __name__ == "__main__":
    sys.exit(main())
