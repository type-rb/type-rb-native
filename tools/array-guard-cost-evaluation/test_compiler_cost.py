import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import compiler_cost


class CollectorEntryTests(unittest.TestCase):
    def collect(self, root, mismatch=False):
        roles = {}
        for role in ("previous", "native", "baseline"):
            binary = root / role / "compiler"
            binary.parent.mkdir()
            binary.write_bytes(role.encode())
            roles[role] = {"revision": role, "path": str(binary)}
        manifest = root / "compilers.json"
        manifest.write_text(json.dumps(roles))
        output = root / "cost"
        calls = []

        def observe(command, directory, timeout, **kwargs):
            role = Path(command[0]).parent.name
            self.assertEqual(command[2], root / "previous/source/compiler/src/compiler.trb")
            self.assertEqual(timeout, 120)
            self.assertEqual(kwargs["core"], 0)
            calls.append(role)
            Path(command[4]).write_bytes(b"wrong" if mismatch else b"previous")
            directory.mkdir(parents=True)
            for name in ("stdout", "stderr"):
                (directory / name).write_bytes(b"")
            return dict(status="pass", exitCode=0, timeoutSeconds=120,
                        wallSeconds=1., cpuSeconds=1., memoryBytes=100)

        argv = ["compiler_cost.py", "--compilers", str(manifest),
                "--qbe", "unused-mocked-qbe", "--output", str(output)]
        with patch.object(compiler_cost.sys, "argv", argv), \
             patch.object(compiler_cost.os, "sched_getaffinity", return_value={0}, create=True), \
             patch.object(compiler_cost, "observe", side_effect=observe):
            if mismatch:
                with self.assertRaisesRegex(ValueError, "fixed point"):
                    compiler_cost.main()
            else:
                compiler_cost.main()
        return calls, json.loads((output / "compiler-cost.json").read_text())

    def test_preparation_schema_runs_all_interleaved_observations(self):
        with tempfile.TemporaryDirectory() as temporary:
            calls, result = self.collect(Path(temporary))
        self.assertEqual(calls, ["previous", "native", "native", "previous",
                                 "previous", "native", "native", "previous"])
        self.assertEqual(result["status"], "pass")
        self.assertEqual(len(result["raw"]), 8)
        self.assertEqual(result["outputIdentities"]["previous"],
                            result["outputIdentities"]["native"])

    def test_first_fixed_point_failure_is_retained_without_more_commands(self):
        with tempfile.TemporaryDirectory() as temporary:
            calls, result = self.collect(Path(temporary), mismatch=True)
        self.assertEqual(calls, ["previous"])
        self.assertEqual(result["status"], "fail")
        self.assertEqual(len(result["raw"]), 1)


if __name__ == "__main__":
    unittest.main()
