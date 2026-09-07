#!/usr/bin/env python3
"""Observe or verify small, path-specific ordinary language cases.

Observation never rewrites expectations. A changed observation needs review;
known rejected cases are coverage gaps, not successful conformance tests.
"""
import argparse
import hashlib
import html
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import tempfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def expected_native(case):
    expected = case["native"]
    if not isinstance(expected, dict) or set(expected) != {"check", "build", "repl"}:
        raise ValueError("missing reviewed Native expectations")
    result = {}
    for action in ("check", "build"):
        diagnostic = expected[action]
        if diagnostic is not None and (not isinstance(diagnostic, str) or not diagnostic):
            raise ValueError("invalid rejection diagnostic")
        result[action] = {"code": 1 if diagnostic else 0,
                          "stdout": "ok\n" if action == "check" and not diagnostic else "",
                          "stderr": diagnostic or ""}
    result["execute"] = None if expected["build"] else {
        "code": 0, "stdout": case["output"], "stderr": ""}
    if (not isinstance(expected["repl"], dict) or set(expected["repl"]) != {"stdout", "stderr"}
            or not all(isinstance(value, str) for value in expected["repl"].values())):
        raise ValueError("invalid REPL expectations")
    result["repl"] = {"code": 0, **expected["repl"]}
    return result


def validate(document):
    if (set(document) != {"schemaVersion", "cases"}
            or type(document["schemaVersion"]) is not int or document["schemaVersion"] != 1):
        raise ValueError("invalid language case registry")
    cases = document["cases"]
    if not isinstance(cases, list) or not cases:
        raise ValueError("empty language cases")
    identities = set()
    for case in cases:
        if (not isinstance(case, dict)
                or set(case) != {"id", "title", "declarations", "body", "output", "referenceRepl", "native"}
                or not all(isinstance(case[key], str) for key in case if key != "native")
                or not re.fullmatch(r"[a-z][a-z0-9-]*", case["id"])
                or not case["title"] or not case["body"]):
            raise ValueError("invalid language case fields")
        if case["id"] in identities:
            raise ValueError("duplicate language case")
        identities.add(case["id"])
        expected_native(case)
    return cases


def coverage_table(cases):
    lines = ["<!-- Generated from tools/native-language-cases.json; do not edit by hand. -->",
             "", "| Case | Check | Build | Execute | REPL |",
             "| --- | --- | --- | --- | --- |"]
    for case in cases:
        expected = expected_native(case)
        check = "accepts" if expected["check"]["code"] == 0 else "rejects"
        build = "accepts" if expected["build"]["code"] == 0 else "rejects"
        execution = "matches reference" if expected["execute"] else "not reached"
        repl = expected["repl"]
        repl_state = ("rejects" if repl["stderr"] else "matches reference"
                      if repl["stdout"] == case["referenceRepl"] else "output differs")
        title = html.escape(case["title"]).replace("|", "&#124;").replace("\n", " ")
        lines.append(f"| {title} | {check} | {build} | {execution} | {repl_state} |")
    return "\n".join(lines) + "\n"


def observe(binary, arguments, root, text=None):
    env = dict(os.environ, NO_COLOR="1", TERM="dumb",
               TRBN_HISTORY=str(root / "native-history.json"))
    child = subprocess.Popen([str(binary), *arguments], cwd=root, env=env,
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True, start_new_session=True)
    timed_out = False
    try:
        stdout, stderr = child.communicate(text, timeout=30)
    except subprocess.TimeoutExpired:
        timed_out = True
        os.killpg(child.pid, signal.SIGKILL)
        stdout, stderr = child.communicate()
    except BaseException:
        if child.poll() is None:
            os.killpg(child.pid, signal.SIGKILL)
        child.communicate()
        raise
    result = {"code": 124 if timed_out else child.returncode,
              "stdout": stdout.replace(str(root), "<case>"),
              "stderr": stderr.replace(str(root), "<case>")}
    if timed_out:
        result["timedOut"] = True
    return result


def collect(case, native, reference, root):
    source = case["declarations"] + "\ndef main()\n" + case["body"] + "\nend\n"
    (root / "main.trb").write_text(source)
    repl = case["declarations"] + "\n" + case["body"] + "\n:quit\n"
    observations = {}
    for role, binary in (("reference", reference), ("native", native)):
        if binary is None:
            continue
        executable = root / (role + "-program")
        result = {"check": observe(binary, ["check", "main.trb"], root)}
        result["build"] = observe(binary, ["build", "--compile", "--outfile",
                                             str(executable), "main.trb"], root)
        if result["build"]["code"] == 0:
            if not executable.is_file():
                raise ValueError(f"{case['id']}: {role} build published no executable")
            result["execute"] = observe(executable, [], root)
        else:
            if executable.exists():
                raise ValueError(f"{case['id']}: failed {role} build published output")
            result["execute"] = None
        result["repl"] = observe(binary, ["repl"], root, repl)
        observations[role] = result
    if reference is None:
        return observations
    reference_result = observations["reference"]
    if reference_result["check"]["code"] != 0 or reference_result["build"]["code"] != 0:
        raise ValueError(f"{case['id']}: invalid reference fixture: {reference_result}")
    if reference_result["execute"] != {"code": 0, "stdout": case["output"], "stderr": ""}:
        raise ValueError(f"{case['id']}: reference output differs: {reference_result}")
    if reference_result["repl"] != {"code": 0, "stdout": case["referenceRepl"], "stderr": ""}:
        raise ValueError(f"{case['id']}: reference REPL differs: {reference_result['repl']}")
    return observations


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--native", type=Path)
    parser.add_argument("--reference", type=Path)
    parser.add_argument("--observe", action="store_true")
    parser.add_argument("--case")
    parser.add_argument("--table", action="store_true")
    parser.add_argument("--check-table", type=Path)
    args = parser.parse_args()
    native = args.native.resolve() if args.native else None
    reference = args.reference.resolve() if args.reference else None
    registry = Path(__file__).with_name("native-language-cases.json")
    document = json.loads(registry.read_text())
    cases = validate(document)
    if args.table or args.check_table:
        if args.case or native or reference or args.observe:
            parser.error("table commands do not execute compilers or select cases")
        table = coverage_table(cases)
        if args.check_table:
            if args.check_table.read_text() != table:
                raise ValueError("coverage table differs from reviewed expectations")
        else:
            print(table, end="")
        return 0
    if native is None and reference is None:
        parser.error("select --native, --reference, or both; no compiler is implicit")
    if args.case:
        cases = [case for case in cases if case["id"] == args.case]
        if not cases:
            raise ValueError("unknown language case")
    report = {"schemaVersion": 1, "nativeSha256": digest(native) if native else None,
              "referenceSha256": digest(reference) if reference else None,
              "registrySha256": digest(registry), "observationOnly": args.observe,
              "typeRBRevision": (registry.parent.parent / "TYPE_RB_REVISION").read_text().strip(),
              "cases": [], "failures": []}
    with tempfile.TemporaryDirectory(prefix="native-language-") as temporary:
        for index, case in enumerate(cases):
            root = Path(temporary).resolve() / str(index)
            root.mkdir()
            try:
                observations = collect(case, native, reference, root)
            except ValueError as error:
                report["cases"].append({"id": case["id"], "error": str(error)})
                report["failures"].append(case["id"])
                continue
            report["cases"].append({"id": case["id"], **observations})
            if native and not args.observe and observations["native"] != expected_native(case):
                report["failures"].append(case["id"])
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
