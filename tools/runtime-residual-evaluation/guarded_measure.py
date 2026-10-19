"""Run the unchanged suite with immediate failure and paired catastrophe stops."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
from backends import BackendRoles


class Guard:
    def __init__(self):
        self.pairs = {}
        self.artifacts = {}

    def check(self, directory, record):
        directory = Path(directory)
        name = directory.name
        if record.get("status") != "pass":
            raise ValueError(f"Stopped after failed observation: {directory}")
        if name == "gc-probe":
            expected = (directory.parent.parent / "expected").read_bytes()
            if (directory / "stdout").read_bytes() != expected:
                raise ValueError("GC output differs")
            stats = {}
            for line in (directory / "stderr").read_text().splitlines():
                prefix, key, value = line.split(",")
                if prefix != "type-rb-native-gc-stat-v1" or key in stats:
                    raise ValueError("Invalid GC counters")
                stats[key] = int(value)
            if (not {"live-bytes", "allocated-bytes", "reclaimed-bytes"}.issubset(stats) or
                    any(value < 0 for value in stats.values()) or stats["live-bytes"] != 0 or
                    stats["allocated-bytes"] != stats["reclaimed-bytes"]):
                raise ValueError("Incomplete GC reclamation")
            return
        if not (name.startswith("build-") or name.startswith("runtime-")):
            return
        role, case = directory.parent.name, directory.parent.parent.name
        artifact = record.get("artifact")
        if name.startswith("build-"):
            # The maintained controller first writes status, then the artifact.
            if artifact is None:
                return
            key = (case, role)
            if key in self.artifacts and self.artifacts[key] != artifact["sha256"]:
                raise ValueError("Repeated build artifact identity differs")
            self.artifacts[key] = artifact["sha256"]
        if role not in ("native", "previous"):
            return
        pair = self.pairs.setdefault((case, name), {})
        pair[role] = record
        if set(pair) != {"native", "previous"}:
            return
        for metric in ("wallSeconds", "cpuSeconds", "memoryBytes"):
            current, previous = pair["native"][metric], pair["previous"][metric]
            if previous > 0 and current > 2 * previous:
                raise ValueError(f"Paired catastrophe: {case}/{name}/{metric}")
        if name.startswith("build-") and pair["native"]["artifact"]["bytes"] > 2 * pair["previous"]["artifact"]["bytes"]:
            raise ValueError(f"Paired artifact catastrophe: {case}/{name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--compilers", required=True)
    parser.add_argument("--qbe", required=True)
    parser.add_argument("--previous-qbe", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    path = args.source_root / "tools/daily-performance/measure.py"
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location("registered_measure", path)
    measure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(measure)
    registration = json.loads(Path(__file__).with_name("registration.json").read_text())
    roles = json.loads(Path(args.compilers).read_text())
    backends = BackendRoles(roles, args.qbe, args.previous_qbe, registration["backends"])
    guard = Guard()
    original_write = measure.write

    def write(path, data):
        if Path(path).name == "context.json" or Path(path) == Path(args.output):
            data["backends"] = backends.identities
        original_write(path, data)  # Preserve the offending observation first.
        path = Path(path)
        if path.name == "observation.json":
            guard.check(path.parent, data)

    original_observe = measure.observe
    def observe(command, *positional, **keywords):
        return original_observe(backends.route(command), *positional, **keywords)
    measure.observe = observe
    measure.write = write
    status = {"status": "started", "changedOrderingOrTimer": False,
              "backendPolicy": "Registered compiler-specific backend argument; every actual command retained",
              "backends": backends.identities}
    try:
        backends.verify_unchanged()
        measure.run(args)
        backends.verify_unchanged()
        status["status"] = "pass"
    except Exception as error:
        status.update(status="fail", error=str(error))
        raise
    finally:
        Path(args.evidence).mkdir(parents=True, exist_ok=True)
        (Path(args.evidence) / "guard-status.json").write_text(json.dumps(status, indent=2) + "\n")


if __name__ == "__main__":
    main()
