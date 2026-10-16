"""One matched, interleaved same-input compiler build comparison: eight observations."""
import argparse
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/daily-performance"))
from measure import digest, observe, summarize


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compilers", type=Path, required=True)
    parser.add_argument("--qbe", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    roles = json.loads(args.compilers.read_text())
    env = {key: value for key, value in os.environ.items()
           if not key.startswith("TYPE_RB_NATIVE_RUNTIME_")}
    env.update(GOFLAGS="-trimpath", GOMAXPROCS="1", LC_ALL="C")
    core = min(os.sched_getaffinity(0))
    source_revision = roles["previous"]["revision"]
    source = args.compilers.parent / source_revision / "source/compiler/src/compiler.trb"
    raw = []
    try:
        for index in range(4):
            order = ("previous", "native") if index % 2 == 0 else ("native", "previous")
            for role in order:
                compiler = roles[role]
                output = args.output / role / "compiler"
                output.parent.mkdir(exist_ok=True)
                record = observe([compiler["path"], "build", source, "--output", output,
                                  "--qbe", args.qbe, "--cc", "/usr/bin/cc", "--target", "linux-arm64-v0"],
                                 args.output / role / f"build-{index}", 120, env=env, core=core)
                record.update(role=role, phase="warmup" if index == 0 else "retained", revision=compiler["revision"], sourceRevision=source_revision)
                raw.append(record)
                if (record["status"] != "pass" or not output.exists()
                        or digest(output) != digest(roles["previous"]["path"])
                        or (args.output / role / f"build-{index}" / "stdout").stat().st_size
                        or (args.output / role / f"build-{index}" / "stderr").stat().st_size):
                    raise ValueError(f"{role}: same-input build differs from the accepted compiler")
                record["binarySha256"] = digest(output)
                record["binaryBytes"] = output.stat().st_size
                output.unlink()
            pair = {row["role"]: row for row in raw[-2:]}
            for metric in ("wallSeconds", "cpuSeconds", "memoryBytes"):
                previous, current = pair["previous"][metric], pair["native"][metric]
                if previous > 0 and current > 2 * previous:
                    raise ValueError(f"Paired compiler catastrophe: {index}/{metric}")
        summaries = {role: summarize([row for row in raw if row["role"] == role], 3) for role in ("native", "previous")}
        result = {"status": "pass", "raw": raw, "summaries": summaries,
                  "ratios": {metric: summaries["native"][metric] / summaries["previous"][metric]
                             for metric in ("wallSeconds", "cpuSeconds", "memoryBytes")},
                  "compilerBytes": {role: Path(roles[role]["path"]).stat().st_size for role in ("native", "previous", "baseline")},
                  "scope": "Same accepted compiler input compiled by both roles; candidate own-source cost recorded separately by daily compiler-self. Cumulative compiler binary size; cumulative self-build timing unmeasured."}
    except Exception as error:
        result = {"status": "fail", "raw": raw, "error": str(error)}
        raise
    finally:
        (args.output / "compiler-cost.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
