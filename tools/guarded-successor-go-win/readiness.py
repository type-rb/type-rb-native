"""Untimed correctness and repeated-build prerequisites for a frozen cohort."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/daily-performance"))
from measure import digest, source_case


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compilers", type=Path, required=True)
    parser.add_argument("--qbe", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    roles = json.loads(args.compilers.read_text())
    roles["pure-go"] = {"path": shutil.which("go")}
    suite = json.loads((ROOT / "tools/daily-performance/suite.json").read_text())
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("TYPE_RB_NATIVE_RUNTIME_")}
    env.update(GOFLAGS="-trimpath", GOMAXPROCS="1", LC_ALL="C")
    rows = []
    try:
        for case in suite["cases"]:
            directory = args.output / case["id"]
            expected = source_case(case, directory)
            if "pureGoSource" in case:
                shutil.copyfile(ROOT / case["pureGoSource"], directory / "pure-go.go")
            for role, compiler in roles.items():
                if role == "pure-go" and "pureGoSource" not in case:
                    continue
                if role == "baseline" and not case.get("frozenBaseline", True):
                    continue
                hashes = []
                for index in range(2):
                    output = directory / role / "program"
                    output.parent.mkdir(exist_ok=True)
                    output.unlink(missing_ok=True)
                    shutil.rmtree(directory / "build", ignore_errors=True)
                    if role == "pure-go":
                        command = [compiler["path"], "build", "-trimpath", "-o", str(output), str(directory / "pure-go.go")]
                    elif role == "typerb-go":
                        command = [compiler["path"], "build", "--compile", "--config", "trbconfig.jsonc", "--outfile", str(output)]
                    else:
                        command = [compiler["path"], "build", str(directory / "src/main.trb"), "--output", str(output),
                                   "--qbe", args.qbe, "--cc", "/usr/bin/cc", "--target", "linux-arm64-v0"]
                    build = subprocess.run(command, cwd=directory, env=env, capture_output=True, timeout=90, check=True)
                    if build.stderr:
                        raise ValueError(f"{case['id']}/{role}: build stderr: {build.stderr.decode(errors='replace')}")
                    run = subprocess.run([str(output), *case["args"]], env=env, capture_output=True, timeout=30, check=True)
                    if run.stdout != expected or run.stderr:
                        raise ValueError(f"{case['id']}/{role}: incorrect output")
                    hashes.append(digest(output))
                if len(set(hashes)) != 1:
                    raise ValueError(f"{case['id']}/{role}: repeated build identity differs")
                rows.append({"case": case["id"], "role": role, "sha256": hashes[0], "builds": 2, "outputs": 2})
                print(f"ready {case['id']} {role}", flush=True)
        if len(rows) != 67:
            raise ValueError("Incomplete readiness matrix")
        current = next(row for row in rows if row["case"] == "allocation" and row["role"] == "native")
        previous = next(row for row in rows if row["case"] == "allocation" and row["role"] == "previous")
        if current["sha256"] == previous["sha256"]:
            raise ValueError("Primary application did not change")
        result = {"status": "pass", "rows": rows, "timingObservations": 0,
                  "goFlags": env["GOFLAGS"], "goVersion": subprocess.check_output(["go", "version"], text=True).strip()}
    except Exception as error:
        result = {"status": "fail", "rows": rows, "error": str(error), "timingObservations": 0}
        raise
    finally:
        (args.output / "readiness.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
