#!/usr/bin/env python3
"""Acquire pinned QBE with the reviewed IL extension and ARM64 selector fixes."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def backend_identity(root=ROOT):
    backend = json.loads((root / "tools/qbe/backend.json").read_text())
    if set(backend) != {"name", "version", "sourceURL", "sourceSHA256", "variant", "patches"}:
        raise ValueError("invalid QBE identity shape")
    if backend["name"] != "QBE" or backend["version"] != "1.3" or backend["variant"] != "typerb-arm64-immediates-v1":
        raise ValueError("unsupported QBE identity")
    if not backend["sourceURL"].startswith("https://") or not re.fullmatch(r"[0-9a-f]{64}", backend["sourceSHA256"]):
        raise ValueError("invalid QBE source identity")
    paths = ["tools/qbe/sqrt.patch", "tools/qbe/arm64-immediates.patch"]
    if len(backend["patches"]) != len(paths):
        raise ValueError("invalid QBE patch set")
    for patch, path in zip(backend["patches"], paths):
        if set(patch) != {"path", "sha256"} or patch["path"] != path:
            raise ValueError("invalid QBE patch identity")
        if digest(root / patch["path"]) != patch["sha256"]:
            raise ValueError("QBE patch digest differs")
    return backend


def check_capability(binary):
    source = ("export function d $probe(d %x) {\n@start\n %y =d sqrt %x\n ret %y\n}\n"
              "export function l $integer(l %x) {\n@start\n %a =l add %x, 7\n"
              " %b =l and %a, 65535\n %c =l sar %b, 65\n ret %c\n}\n")
    for target, instruction in (("arm64_apple", "fsqrt"), ("arm64", "fsqrt"), ("amd64_sysv", "sqrtsd")):
        result = subprocess.run([str(binary), "-t", target], input=source, text=True,
                                capture_output=True, timeout=30)
        if result.returncode or instruction not in result.stdout:
            raise ValueError(f"QBE lacks the required {target} sqrt operation: {result.stderr.strip()}")
        if target.startswith("arm64"):
            for operation, constant in (("add", "7"), ("and", "65535"), ("asr", "1")):
                if not re.search(rf"\b{operation}\s+[^\n]*, #{constant}\s*$", result.stdout, re.MULTILINE):
                    raise ValueError(f"QBE lacks the required {target} integer immediate selection")


def build(output, archive=None):
    backend = backend_identity()
    output = output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    cc = Path(os.environ.get("CC", "/usr/bin/cc")).resolve()
    if not cc.is_file():
        raise ValueError("QBE C compiler is not an executable file")
    inputs = {"backend": backend, "builderSHA256": digest(__file__), "ccSHA256": digest(cc),
              "platform": sys.platform, "machine": os.uname().machine}
    receipt = output / "build-info.json"
    binary = output / "qbe"
    if receipt.is_file() and binary.is_file():
        previous = json.loads(receipt.read_text())
        if previous.get("inputs") == inputs and previous.get("binarySHA256") == digest(binary):
            return binary
    archive = Path(archive).resolve() if archive else output.parent / "qbe-1.3.tar.xz"
    with tempfile.TemporaryDirectory(prefix="qbe-build-", dir=output.parent) as temporary:
        stage = Path(temporary)
        if not archive.is_file():
            download = stage / "source.tar.xz"
            subprocess.run(["curl", "--fail", "--location", "--retry", "3", backend["sourceURL"],
                            "-o", str(download)], check=True)
            if digest(download) != backend["sourceSHA256"]:
                raise ValueError("QBE archive digest differs")
            archive.parent.mkdir(parents=True, exist_ok=True)
            os.replace(download, archive)
        if digest(archive) != backend["sourceSHA256"]:
            raise ValueError("QBE archive digest differs")
        subprocess.run(["tar", "-xf", str(archive), "-C", str(stage)], check=True)
        source = stage / "qbe-1.3"
        for patch in backend["patches"]:
            subprocess.run(["patch", "--batch", "--fuzz=0", "-p1", "-i", str(ROOT / patch["path"])],
                           cwd=source, check=True, stdout=sys.stderr)
        subprocess.run(["make", "-j2", f"CC={cc}"], cwd=source, check=True, stdout=sys.stderr)
        check_capability(source / "qbe")
        output.mkdir(parents=True, exist_ok=True)
        staged_binary = stage / "published-qbe"
        shutil.copy2(source / "qbe", staged_binary)
        info = {"inputs": inputs, "binarySHA256": digest(staged_binary)}
        staged_receipt = stage / "build-info.json"
        staged_receipt.write_text(json.dumps(info, indent=2) + "\n")
        os.replace(staged_binary, binary)
        os.replace(staged_receipt, receipt)
    return binary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, nargs="?")
    parser.add_argument("--archive", type=Path)
    parser.add_argument("--check", type=Path)
    parser.add_argument("--identity", action="store_true")
    args = parser.parse_args()
    try:
        if args.identity:
            print(json.dumps(backend_identity(), sort_keys=True))
        elif args.check:
            backend_identity()
            check_capability(args.check.resolve())
        elif args.output:
            print(build(args.output, args.archive))
        else:
            parser.error("provide an output directory, --check or --identity")
    except (ValueError, OSError, subprocess.SubprocessError) as error:
        print(f"qbe-toolchain: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
