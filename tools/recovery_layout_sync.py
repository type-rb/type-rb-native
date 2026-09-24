#!/usr/bin/env python3
"""Synchronize recovery inventories with the canonical compiler closure.

The closure is every compiler module reachable through imports from
compiler/src/compiler.trb. Three hand-read inventories must match it:

- src/compiler_recovery_layout.trb: one row per module with its exact import
  header, in the recovery flattening order;
- src/compiler_recovery_mutations.trb: one observable source mutation per
  module except the entry, whose needle occurs exactly once; and
- the module list parsed by compiler/src/compiler_test.trb's own-frontend test.

--check reports drift. --write adds and removes rows, resynchronizes import
headers and generates a default mutation for a module without a usable one.
"""

import argparse
import json
import re
from pathlib import Path


LAYOUT = "src/compiler_recovery_layout.trb"
MUTATIONS = "src/compiler_recovery_mutations.trb"
FRONTEND_TEST = "compiler/src/compiler_test.trb"
FRONTEND_TEST_NAME = "parses the checked-in compiler closure through its own frontend"
STRING = r'"(?:\\.|[^"\\])*"'
LAYOUT_ROW = re.compile(
    r'(?m)^\t\tRecoveryCompilerModule\.new\(name: "([^"]+)", imports: (' + STRING + r')\),\n'
)
MUTATION_ROW = re.compile(r'(?m)^\t\t\[(' + STRING + r'), (' + STRING + r'), (' + STRING + r')\],\n')
IMPORT = re.compile(r"import (?:\{[^}]*\} from )?([A-Za-z0-9_/]+)")
SAFE_LITERAL = re.compile(r'"([A-Za-z0-9 _.,:;!?()<>=+*/-]{3,})"')
FIELD = re.compile(r"\t[a-z_][a-z0-9_]*: [^\n#]+")


class InventoryError(ValueError):
    pass


def canonical_imports(source: str) -> str:
    lines = source.splitlines(keepends=True)
    count = 0
    while count < len(lines) and lines[count].startswith("import "):
        count += 1
    if any(line.startswith("import ") for line in lines[count:]):
        raise InventoryError("imports must form the leading block of a compiler module")
    if count == 0:
        return ""
    if count < len(lines) and lines[count] == "\n":
        count += 1
    return "".join(lines[:count])


def closure(root: Path) -> list[str]:
    """Modules reachable from the compiler entry, in discovery order."""
    directory = root / "compiler/src"
    found: list[str] = []
    pending = ["compiler"]
    while pending:
        name = pending.pop(0)
        if name in found:
            continue
        path = directory / f"{name}.trb"
        if not path.is_file():
            raise InventoryError(f"missing canonical compiler module {name}")
        found.append(name)
        try:
            header = canonical_imports(path.read_text())
        except InventoryError as error:
            raise InventoryError(f"{name}: {error}") from None
        for line in header.splitlines():
            match = IMPORT.match(line)
            target = match and match.group(1)
            if target and "/" not in target and (directory / f"{target}.trb").is_file():
                pending.append(target)
    return found


def encode(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def decode(literal: str) -> str:
    # Inventory strings use the JSON-compatible subset of TypeRB escapes.
    return json.loads(literal)


def default_mutation(name: str, source: str) -> list[str] | None:
    """A well-typed edit that must change the emitted compiler QBE."""
    body = source[len(canonical_imports(source)):]
    for match in SAFE_LITERAL.finditer(body):
        needle = match.group(0)
        if source.count(needle) == 1:
            return [name, needle, needle[:-1] + '~"']
    lines = body.splitlines()
    for index in range(len(lines) - 1):
        first, second = lines[index], lines[index + 1]
        if FIELD.fullmatch(first) and FIELD.fullmatch(second) and first != second:
            needle = first + "\n" + second
            if source.count(needle) == 1:
                return [name, needle, second + "\n" + first]
    return None


def sync_layout(root: Path, modules: list[str], sources: dict[str, str], write: bool) -> list[str]:
    path = root / LAYOUT
    original = path.read_text()
    rows = LAYOUT_ROW.findall(original)
    if len(rows) != original.count("RecoveryCompilerModule.new(name:"):
        raise InventoryError("recovery layout contains an unrecognized module row")
    names = [name for name, _ in rows]
    if len(set(names)) != len(names):
        raise InventoryError("duplicate recovery module")
    changes = [f"layout: add {name}" for name in modules if name not in names]
    changes += [f"layout: remove {name}" for name in names if name not in modules]

    def replace(match: re.Match[str]) -> str:
        name, encoded = match.group(1), match.group(2)
        if name not in modules:
            return ""
        expected = encode(canonical_imports(sources[name]))
        if encoded != expected:
            changes.append(f"layout: imports {name}")
        return match.group(0).replace(encoded, expected)

    updated = LAYOUT_ROW.sub(replace, original)
    additions = "".join(
        f'\t\tRecoveryCompilerModule.new(name: "{name}", imports: {encode(canonical_imports(sources[name]))}),\n'
        for name in modules if name not in names)
    closing = updated.rindex("\t]\n")
    updated = updated[:closing] + additions + updated[closing:]
    if write and updated != original:
        path.write_text(updated)
    return changes


def sync_mutations(root: Path, modules: list[str], sources: dict[str, str], write: bool) -> list[str]:
    path = root / MUTATIONS
    original = path.read_text()
    rows = MUTATION_ROW.findall(original)
    if len(rows) != original.count('\t\t["'):
        raise InventoryError("recovery mutations contain an unrecognized row")
    changes: list[str] = []
    seen: set[str] = set()
    targets = [name for name in modules if name != "compiler"]
    kept: list[str] = []
    for match in MUTATION_ROW.finditer(original):
        name, needle, replacement = (decode(literal) for literal in match.groups())
        if name not in targets or name in seen:
            changes.append(f"mutations: remove {name}")
            continue
        seen.add(name)
        if needle == replacement or sources[name].count(needle) != 1:
            generated = default_mutation(name, sources[name])
            if generated is None:
                raise InventoryError(f"mutation for {name} no longer matches once; add one by hand")
            changes.append(f"mutations: regenerate {name}")
            kept.append("\t\t[" + ", ".join(encode(value) for value in generated) + "],\n")
            continue
        kept.append(match.group(0))
    for name in targets:
        if name not in seen:
            generated = default_mutation(name, sources[name])
            if generated is None:
                raise InventoryError(f"no default mutation for {name}; add one by hand")
            changes.append(f"mutations: add {name}")
            kept.append("\t\t[" + ", ".join(encode(value) for value in generated) + "],\n")
    first = MUTATION_ROW.search(original)
    closing = original.rindex("\t]\n")
    updated = original[:first.start()] + "".join(kept) + original[closing:] if first else original
    if write and updated != original:
        path.write_text(updated)
    return changes


def sync_frontend_test(root: Path, modules: list[str], write: bool) -> list[str]:
    path = root / FRONTEND_TEST
    original = path.read_text()
    test = original.find(FRONTEND_TEST_NAME)
    start = original.find("names := [", test)
    finish = original.find("]", start)
    if test < 0 or start < 0 or finish < 0:
        raise InventoryError("own-frontend module list is missing")
    names = re.findall(r'"([a-z0-9_]+)"', original[start:finish])
    if not names or names[0] != "compiler":
        raise InventoryError("own-frontend module list must start with the compiler entry")
    kept = [name for name in names if name in modules]
    kept += [name for name in modules if name not in kept]
    changes = [f"frontend test: add {name}" for name in modules if name not in names]
    changes += [f"frontend test: remove {name}" for name in names if name not in modules]
    updated = original[:start] + "names := [" + ", ".join(f'"{name}"' for name in kept) + original[finish:]
    if write and updated != original:
        path.write_text(updated)
    return changes


def synchronize(root: Path, write: bool) -> list[str]:
    modules = closure(root)
    sources = {name: (root / "compiler/src" / f"{name}.trb").read_text() for name in modules}
    return (sync_layout(root, modules, sources, write) +
            sync_mutations(root, modules, sources, write) +
            sync_frontend_test(root, modules, write))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    try:
        changes = synchronize(root, args.write)
    except InventoryError as error:
        print(f"Recovery inventory error: {error}")
        return 1
    if changes:
        print("Recovery inventories differ from the compiler closure:")
        for change in changes:
            print(f"  {change}")
        if args.check:
            print("Run python3 tools/recovery_layout_sync.py --write")
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
