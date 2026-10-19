"""Exercise compiler preparation with fake tools, never product binaries."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


class PreparationRoutingTests(unittest.TestCase):
    def test_every_generation_uses_the_backend_for_its_source_role(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            binaries = root / "fake-tools"
            binaries.mkdir()
            suite = root / "tools/daily-performance/suite.json"
            suite.parent.mkdir(parents=True)
            suite.write_text(json.dumps({"baseline": "c" * 40}))
            (root / "TYPE_RB_REVISION").write_text("d" * 40)
            log = root / "calls.jsonl"

            def executable(path, body):
                path.write_text("#!" + sys.executable + "\n" + body)
                path.chmod(0o755)

            executable(binaries / "git", '''import pathlib, sys
args = sys.argv[1:]
if args == ['rev-parse', 'HEAD']:
    print('a' * 40)
elif args[:2] == ['worktree', 'add']:
    source = pathlib.Path(args[3]) / 'compiler/src/compiler.trb'
    source.parent.mkdir(parents=True)
    source.write_text('synthetic source; never compiled')
elif args[:2] != ['merge-base', '--is-ancestor']:
    raise SystemExit('unexpected git command')
''')
            executable(binaries / "strace", '''import json, os, pathlib, sys
args = sys.argv[1:]
trace = args.index('-o')
pathlib.Path(args[trace + 1]).write_text('')
command = args[trace + 2:]
output = pathlib.Path(command[command.index('--output') + 1])
output.write_bytes(b'synthetic compiler; never executed')
with open(os.environ['BACKEND_TEST_LOG'], 'a') as log:
    log.write(json.dumps({'kind':'generation','command':command}) + '\\n')
''')
            bootstrap = root / "tools/bootstrap-seed.sh"
            # The maintained wrapper explicitly invokes /bin/sh for bootstrap.
            bootstrap.write_text('''#!/bin/sh
exec "$BACKEND_TEST_PYTHON" "$BACKEND_TEST_BOOTSTRAP" "$@"
''')
            fake_bootstrap = binaries / "bootstrap.py"
            executable(fake_bootstrap, '''import json, os, pathlib, sys
args = sys.argv[1:]
pathlib.Path(args[args.index('--output') + 1]).write_bytes(b'synthetic fixed point')
pathlib.Path(args[args.index('--evidence') + 1]).mkdir(parents=True)
with open(os.environ['BACKEND_TEST_LOG'], 'a') as log:
    log.write(json.dumps({'kind':'bootstrap','command':args}) + '\\n')
''')
            seed, baseline_seed, current_qbe, previous_qbe = [root / name for name in
                ("seed", "baseline-seed", "current-qbe", "previous-qbe")]
            for path in (seed, baseline_seed, current_qbe, previous_qbe):
                path.write_text("synthetic input; never executed")
                path.chmod(0o755)
            workspace = root / "compilers"
            environment = dict(os.environ, PATH=str(binaries) + os.pathsep + os.environ["PATH"],
                               RUNNER_TEMP=str(root), BACKEND_TEST_LOG=str(log),
                               BACKEND_TEST_PYTHON=sys.executable,
                               BACKEND_TEST_BOOTSTRAP=str(fake_bootstrap))
            script = Path(__file__).with_name("prepare_compilers.sh")
            result = subprocess.run(["/bin/sh", str(script), str(seed), str(current_qbe),
                                     "b" * 40, str(previous_qbe), str(workspace), str(baseline_seed)],
                                    cwd=root, env=environment, capture_output=True, text=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            calls = [json.loads(line) for line in log.read_text().splitlines()]
            self.assertEqual(len(calls), 9)
            for index, revision in enumerate(("a" * 40, "b" * 40, "c" * 40)):
                expected_qbe = current_qbe if index == 0 else previous_qbe
                for row in calls[index * 3:index * 3 + 3]:
                    command = row["command"]
                    self.assertEqual(command[command.index("--qbe") + 1], str(expected_qbe))
                    self.assertIn(str(workspace / revision / "source"), " ".join(command))
                first = calls[index * 3]["command"]
                self.assertEqual(first[0], str(baseline_seed if index == 2 else seed))
            roles = json.loads((workspace / "compilers.json").read_text())
            self.assertEqual(set(roles), {"native", "previous", "baseline", "typerb-go"})
            self.assertEqual(roles["native"]["revision"], "a" * 40)
            self.assertEqual(roles["baseline"]["revision"], "c" * 40)


if __name__ == "__main__":
    unittest.main()
