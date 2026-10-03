#!/usr/bin/env python3
"""Sync or verify the bundled official sources against pinned reference Git objects."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = "internal/official/packages"
BUNDLE = Path("vendor/type-rb/official")
CATALOG = Path("compiler/src/project/official_catalog.trb")
REPOSITORY = "https://github.com/type-rb/type-rb"


class ValidationError(Exception):
    pass


def git(checkout, *args):
    result = subprocess.run(["git", "--no-replace-objects", "-C", str(checkout), *args], capture_output=True)
    if result.returncode:
        raise ValidationError("cannot read pinned reference Git objects: " +
                              result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def reference_files(root, checkout):
    revision = (root / "TYPE_RB_REVISION").read_text().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValidationError("TYPE_RB_REVISION must be an exact commit id")
    if git(checkout, "cat-file", "-t", revision).strip() != b"commit":
        raise ValidationError("TYPE_RB_REVISION must identify a commit")
    files = {}
    entries = git(checkout, "ls-tree", "-rz", "--full-tree", revision, "--", SOURCE_ROOT)
    for entry in entries.split(b"\0"):
        if not entry:
            continue
        metadata, raw_path = entry.split(b"\t", 1)
        mode, kind, oid = metadata.split()
        source_path = raw_path.decode("utf-8")
        relative = source_path.removeprefix(SOURCE_ROOT + "/")
        path = PurePosixPath(relative)
        if (source_path == relative or path.is_absolute() or ".." in path.parts or
                path.as_posix() != relative or "\\" in relative):
            raise ValidationError("invalid reference package path: " + source_path)
        if mode != b"100644" or kind != b"blob":
            raise ValidationError("reference package must be a regular file: " + source_path)
        files["packages/" + relative] = git(checkout, "cat-file", "blob", oid.decode("ascii"))
    if not files or not any(name.endswith("/trbpackage.json") for name in files):
        raise ValidationError("pinned reference has no official package manifests")
    license_entry = git(checkout, "ls-tree", revision, "--", "LICENSE").split()
    if len(license_entry) != 4 or license_entry[:2] != [b"100644", b"blob"]:
        raise ValidationError("pinned reference license must be a regular file")
    files["LICENSE"] = git(checkout, "cat-file", "blob", license_entry[2].decode("ascii"))
    provenance = {
        "schemaVersion": 1,
        "repository": REPOSITORY,
        "revision": revision,
        "sourceRoot": SOURCE_ROOT,
        "files": [
            {"path": name,
             "source": "LICENSE" if name == "LICENSE" else SOURCE_ROOT + "/" + name[len("packages/"):],
             "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            for name, data in sorted(files.items())
        ],
    }
    files["provenance.json"] = (json.dumps(provenance, indent=2) + "\n").encode("utf-8")
    return files


def bundle_files(root):
    bundle = root / BUNDLE
    for path in (root / "vendor", root / "vendor/type-rb", bundle):
        if path.is_symlink():
            raise ValidationError("bundle contains a symlink: " + str(path))
    if not bundle.is_dir():
        raise ValidationError("official source bundle is missing")
    files = {}
    for directory, directories, names in os.walk(bundle, followlinks=False):
        for name in directories + names:
            path = Path(directory) / name
            if path.is_symlink():
                raise ValidationError("bundle contains a symlink: " + str(path.relative_to(bundle)))
        for name in names:
            path = Path(directory) / name
            if not path.is_file():
                raise ValidationError("bundle entry must be a regular file: " + str(path))
            files[path.relative_to(bundle).as_posix()] = path.read_bytes()
    return files


def typerb_string(value):
    # Escape interpolation after escaping backslashes, preserving the raw value.
    return json.dumps(value, ensure_ascii=False).replace("#{", "\\#{")


def catalog_source(files):
    packages = []
    names = set()
    for path, data in sorted(files.items()):
        if not path.endswith("/trbpackage.json"):
            continue
        manifest = json.loads(data)
        name, module, source = (manifest[key] for key in ("name", "module", "source"))
        if not all(isinstance(value, str) and value for value in (name, module, source)):
            raise ValidationError("official catalog requires name, module and source: " + path)
        source_path = PurePosixPath(path).parent / source
        if source_path.is_absolute() or ".." in source_path.parts or source_path.as_posix() not in files:
            raise ValidationError("invalid official catalog source: " + path)
        aliases = manifest.get("aliases", [])
        if not isinstance(aliases, list) or not all(isinstance(alias, str) and alias for alias in aliases):
            raise ValidationError("invalid official catalog aliases: " + path)
        for key in [name, *aliases]:
            if key in names:
                raise ValidationError("duplicate official catalog name: " + key)
            names.add(key)
        supported = (manifest.get("kind", "portable") == "portable" and
                     not manifest.get("targets") and
                     not any(manifest.get(key) for key in ("semanticProvider", "typeProvider", "projectProvider")))
        packages.append((name, aliases, module, files[source_path.as_posix()].decode("utf-8"), supported))
    lines = ["# Generated by tools/official-sources.py from the pinned reference bundle.",
             "# Source String values preserve the upstream bytes; do not edit this catalog.", "",
             "def official_source_kind(path: String): Integer"]
    for index, (name, aliases, *_rest) in enumerate(packages, 100):
        condition = " || ".join("path == " + typerb_string(key) for key in [name, *aliases])
        lines += ["\tif " + condition, "\t\treturn " + str(index), "\tend"]
    lines += ["\treturn 0", "end", ""]
    for function, type_name, column, default in (("official_source_name", "String", 2, '""'),
                                               ("official_source_text", "String", 3, '""'),
                                               ("official_source_supported", "Boolean", 4, "false")):
        lines += [f"def {function}(kind: Integer): {type_name}"]
        for index, package in enumerate(packages, 100):
            value = package[column]
            literal = ("true" if value else "false") if isinstance(value, bool) else typerb_string(value)
            lines += ["\tif kind == " + str(index), "\t\treturn " + literal, "\tend"]
        lines += ["\treturn " + default, "end", ""]
    return "\n".join(lines).encode("utf-8")


def catalog_path(root):
    destination = root / CATALOG
    for path in [destination, *destination.parents]:
        if path == root:
            break
        if path.is_symlink():
            raise ValidationError("official catalog contains a symlink: " + str(path))
    return destination


def check(root, checkout):
    expected = reference_files(root, checkout)
    actual = bundle_files(root)
    missing = sorted(expected.keys() - actual.keys())
    extra = sorted(actual.keys() - expected.keys())
    if missing:
        raise ValidationError("official source bundle is missing: " + missing[0])
    if extra:
        raise ValidationError("official source bundle has an unexpected file: " + extra[0])
    for name in sorted(expected):
        if actual[name] != expected[name]:
            raise ValidationError("official source bundle differs from TYPE_RB_REVISION: " + name)
    catalog = catalog_path(root)
    if not catalog.is_file() or catalog.read_bytes() != catalog_source(expected):
        raise ValidationError("official source catalog differs from TYPE_RB_REVISION")
    return len(expected) - 1


def sync(root, checkout):
    expected = reference_files(root, checkout)
    catalog_bytes = catalog_source(expected)
    catalog = catalog_path(root)
    bundle = root / BUNDLE
    for path in (root / "vendor", root / "vendor/type-rb", bundle):
        if path.is_symlink():
            raise ValidationError("bundle contains a symlink: " + str(path))
    if bundle.exists():
        bundle_files(root)
    bundle.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="official-sources-", dir=bundle.parent) as tmp:
        staging = Path(tmp) / "bundle"
        for name, data in expected.items():
            destination = staging / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
        backup = Path(tmp) / "previous"
        if bundle.exists():
            bundle.rename(backup)
        try:
            staging.rename(bundle)
        except OSError:
            if backup.exists():
                backup.rename(bundle)
            raise
    catalog.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix="official-catalog-", dir=catalog.parent, delete=False) as staged:
        staged.write(catalog_bytes)
        staged_path = Path(staged.name)
    try:
        staged_path.replace(catalog)
    finally:
        staged_path.unlink(missing_ok=True)
    return len(expected) - 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-checkout", required=True, type=Path)
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check", action="store_true")
    action.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        count = (sync if args.write else check)(ROOT, args.reference_checkout)
    except (ValidationError, OSError, UnicodeError, ValueError) as error:
        print("official sources: " + str(error), file=sys.stderr)
        return 1
    print(f"official sources: {'synced' if args.write else 'verified'} {count} pinned files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
