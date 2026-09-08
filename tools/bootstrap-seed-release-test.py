#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("seed_release", Path(__file__).with_name("bootstrap-seed-release.py"))
seed = importlib.util.module_from_spec(spec)
spec.loader.exec_module(seed)


class SeedReleaseTests(unittest.TestCase):
    def test_active_ci_consumers_authenticate_the_current_seed(self):
        root = Path(__file__).resolve().parent.parent
        for name in ("static-string-compactness", "runtime-worker-memory",
                     "benchmarksgame-formal", "benchmarksgame-build-formal",
                     "gate6n-linux-amd64"):
            with self.subTest(workflow=name):
                workflow = (root / ".github/workflows" / (name + ".yml")).read_text()
                self.assertIn("bootstrap-seed-2026-09-08-loop-transfers", workflow)
                self.assertIn("1d53ed0f5b9471335c913dd9d148ff3b9eb1b483", workflow)
                self.assertIn("tools/bootstrap-seed-download.sh", workflow)
        workflow = (root / ".github/workflows/gate6n-linux-amd64.yml").read_text()
        self.assertIn("ROOT_RELEASE_TAG: bootstrap-seed-2026-08-30", workflow)
        self.assertIn("path: .gate6n-seed-source", workflow)
        self.assertIn('"$GITHUB_WORKSPACE/.gate6n-seed-source"', workflow)
        self.assertIn("AMD64_LOOP_SETUP_REVISION: 4e1d0b4aee97b9a5bd73a98f918b31d47985da25", workflow)
        self.assertIn('"$GITHUB_WORKSPACE/.gate6n-loop-source"', workflow)

    def test_amd64_bridge_does_not_replace_ordinary_candidate_input(self):
        observer = Path(__file__).with_name("gate6n-linux-amd64.sh").read_text()
        self.assertIn('"$root_compiler" emit-qbe "$seed_entry"', observer)
        self.assertIn('runtime_seed=$first_transition', observer)
        self.assertIn('"$first_transition" emit-qbe "$loop_entry"', observer)
        self.assertIn('runtime_seed=$loop_transition', observer)
        self.assertIn('"$runtime_seed" emit-qbe "$compiler_entry"', observer)
        self.assertIn('4e1d0b4aee97b9a5bd73a98f918b31d47985da25 || fail "loop source revision differs"', observer)
        self.assertIn('require_clean_revision "$loop_source_root"', observer)
        self.assertIn('21f507e7ee7de2577f4137f6dfb9f732c14c1640 || fail "seed source revision differs"', observer)
        self.assertIn('require_clean_revision "$seed_source_root"', observer)
        self.assertIn('compiler/conformance/valid/logical-short-circuit.trb', observer)
        self.assertIn("printf 'ok\\n' > \"$evidence/setup/logical-condition.expected\"", observer)
        self.assertIn('cmp "$evidence/setup/logical-condition.expected" "$evidence/setup/logical-condition.stdout"', observer)
        self.assertNotIn('require_empty_file "$evidence/setup/logical-condition.stdout"', observer)

    def test_refresh_roles_match_the_existing_compatibility_boundary(self):
        observer = Path(__file__).with_name("bootstrap-seed-refresh.sh").read_text()
        self.assertIn('build_step "$seed" setup-first setup', observer)
        self.assertIn('build_step "$workspace/setup-first/compiler" setup-runtime setup', observer)
        self.assertIn('for step in b2 b3 b4; do\n    build_step "$seed" "$step" ordinary', observer)
        self.assertIn('if test "$mode" = verify; then\n    cmp "$input" "$workspace/b4/compiler"', observer)

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.inputs = self.root / "inputs"
        self.inputs.mkdir()
        self.revision = "a" * 40
        for name, os_name, runner, target, limit in seed.TARGETS:
            asset = "type-rb-native-bootstrap-" + name
            binary = self.inputs / asset
            binary.write_bytes(("synthetic " + name).encode())
            checksum = seed.digest(binary)
            metadata = {"asset": asset, "profile": name + "-v0", "os": os_name,
                        "architecture": "arm64", "runnerImage": runner, "qbeTarget": target,
                        "ccBoundary": "system-cc", "mode": "0755", "size": binary.stat().st_size,
                        "sha256": checksum, "attestationSubjectSha256": checksum,
                        "qbeBinarySize": 100, "qbeBinarySha256": "b" * 64}
            (self.inputs / (name + ".json")).write_text(json.dumps(metadata))
        self.package = self.root / "package"
        seed.create(self.revision, self.inputs, self.package)
        self.manifest_path = self.package / seed.MANIFEST
        self.manifest = seed.read_json(self.manifest_path)
        self.asset = self.manifest["targets"][0]["asset"]
        self.release = {"tag_name": seed.TAG, "target_commitish": self.revision,
                        "draft": False, "prerelease": True, "immutable": True,
                        "assets": [{"name": p.name, "size": p.stat().st_size, "digest": "sha256:" + seed.digest(p)}
                                   for p in sorted(self.package.iterdir())]}
        self.release_path = self.root / "release.json"
        self.release_path.write_text(json.dumps(self.release))

    def verify(self):
        seed.verify(seed.TAG, self.revision, self.asset, self.package, self.release_path)

    def test_both_targets_and_repeatable_package(self):
        for target in self.manifest["targets"]:
            seed.verify(seed.TAG, self.revision, target["asset"], self.package, self.release_path)
        repeated = self.root / "repeated"
        seed.create(self.revision, self.inputs, repeated)
        for path in self.package.iterdir():
            self.assertEqual(path.read_bytes(), (repeated / path.name).read_bytes())
        with self.assertRaises(FileExistsError):
            seed.create(self.revision, self.inputs, self.package)

    def test_manifest_rejects_changed_identity_or_unknown_fields(self):
        mutations = [
            lambda m: m.update(unexpected=True), lambda m: m.update(schemaVersion=True),
            lambda m: m.update(schemaVersion=1), lambda m: m.update(releaseTag="latest"),
            lambda m: m.update(nativeRevision="c" * 40), lambda m: m.update(status="stable"),
            lambda m: m["predecessor"].update(releaseTag="other"),
            lambda m: m["predecessor"]["targets"][0].update(sha256="c" * 64),
            lambda m: m["backend"].update(version="other"),
            lambda m: m["targets"].reverse(), lambda m: m["targets"].pop(),
        ]
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                manifest = copy.deepcopy(self.manifest)
                mutate(manifest)
                with self.assertRaises(ValueError):
                    seed.validate_manifest(manifest, self.revision)

    def test_target_shape_types_limits_and_provenance(self):
        mutations = {"unexpected": 1, "size": True, "sha256": "X" * 64,
                     "attestationSubjectSha256": "c" * 64, "qbeBinarySize": -1,
                     "qbeBinarySha256": "c", "ccBoundary": "wrapper", "mode": "0777",
                     "runnerImage": "self-hosted", "architecture": "amd64"}
        for index, target in enumerate(self.manifest["targets"]):
            for field, value in mutations.items():
                with self.subTest(index=index, field=field):
                    changed = copy.deepcopy(target)
                    changed[field] = value
                    with self.assertRaises(ValueError):
                        seed.validate_target(changed, seed.TARGETS[index])
            target["size"] = seed.TARGETS[index][4] + 1
            with self.assertRaises(ValueError):
                seed.validate_target(target, seed.TARGETS[index])

    def test_registered_predecessors_remain_tag_bound(self):
        for tag in seed.PREDECESSORS:
            manifest = copy.deepcopy(self.manifest)
            manifest["releaseTag"] = tag
            manifest["predecessor"] = seed.PREDECESSORS[tag]
            seed.validate_manifest(manifest, self.revision, tag)
            for other in seed.PREDECESSORS:
                if other != tag:
                    with self.assertRaises(ValueError):
                        seed.validate_manifest(manifest, self.revision, other)
        for tag in ("latest", "bootstrap-seed-2099-01-01", None, []):
            with self.assertRaises(ValueError):
                seed.validate_manifest(self.manifest, self.revision, tag)

    def test_download_verification_preserves_the_previous_tag(self):
        for tag in ("bootstrap-seed-2026-09-07", "bootstrap-seed-2026-09-08"):
            self.manifest["releaseTag"] = tag
            self.manifest["predecessor"] = seed.PREDECESSORS[tag]
            self.manifest_path.write_text(json.dumps(self.manifest))
            names = [target["asset"] for target in self.manifest["targets"]] + [seed.MANIFEST]
            (self.package / "SHA256SUMS").write_text("".join(
                seed.digest(self.package / name) + "  " + name + "\n" for name in names))
            self.release["tag_name"] = tag
            self.release["assets"] = [{"name": p.name, "size": p.stat().st_size,
                                       "digest": "sha256:" + seed.digest(p)}
                                      for p in sorted(self.package.iterdir())]
            self.release_path.write_text(json.dumps(self.release))
            for target in self.manifest["targets"]:
                seed.verify(tag, self.revision, target["asset"], self.package, self.release_path)
        with self.assertRaises(ValueError):
            self.verify()

    def test_corruption_and_checksum_reordering_fail(self):
        (self.package / self.asset).write_bytes(b"changed")
        with self.assertRaises(ValueError):
            self.verify()
        (self.package / self.asset).write_bytes((self.inputs / self.asset).read_bytes())
        sums = self.package / "SHA256SUMS"
        sums.write_text("\n".join(reversed(sums.read_text().splitlines())) + "\n")
        with self.assertRaises(ValueError):
            self.verify()

    def test_release_state_and_complete_asset_set(self):
        mutations = [lambda r: r.update(draft=True), lambda r: r.update(immutable=False),
                     lambda r: r.update(prerelease=False), lambda r: r.update(tag_name="other"),
                     lambda r: r.update(target_commitish="main"), lambda r: r["assets"].pop(),
                     lambda r: r["assets"].append(r["assets"][0]),
                     lambda r: r["assets"][0].update(digest="sha256:" + "c" * 64)]
        for mutate in mutations:
            release = copy.deepcopy(self.release)
            mutate(release)
            self.release_path.write_text(json.dumps(release))
            with self.assertRaises(ValueError):
                self.verify()

    def test_duplicate_json_keys_and_nonfinite_numbers_fail(self):
        for text in ('{"key":1,"key":2}', '{"value":NaN}', '{"value":Infinity}'):
            self.release_path.write_text(text)
            with self.assertRaises(ValueError):
                seed.read_json(self.release_path)

    def test_bad_input_does_not_create_package(self):
        (self.inputs / self.asset).write_bytes(b"corrupt")
        output = self.root / "not-created"
        with self.assertRaises(ValueError):
            seed.create(self.revision, self.inputs, output)
        self.assertFalse(output.exists())

    def test_all_retained_observations_are_checked(self):
        path = self.root / "observations.csv"
        header = "stage,iteration,elapsed_seconds,peak_rss_bytes,status,cpu_seconds\n"
        for role, stages in (("ordinary", ("b1-b2", "b2-b3", "b3-b4")),
                             ("transition", ("b2-b3", "b3-b4"))):
            rows = [f"{stage},{iteration},1,100,0,1\n" for stage in stages for iteration in range(1, 8)]
            path.write_text(header + "".join(rows))
            seed.observations(path, role)
            for index in range(len(rows)):
                for old, new in ((",1,100,0,1", ",2.1,100,0,1"),
                                 (",1,100,0,1", ",1,201,0,1"),
                                 (",1,100,0,1", ",1,100,0,2.1"),
                                 (",1,100,0,1", ",NaN,100,0,1"),
                                 (",1,100,0,1", ",1,100,1,1")):
                    changed = rows.copy()
                    changed[index] = changed[index].replace(old, new)
                    path.write_text(header + "".join(changed))
                    with self.assertRaises(ValueError):
                        seed.observations(path, role)
            path.write_text(header + "".join(rows[:-1]))
            with self.assertRaises(ValueError):
                seed.observations(path, role)


if __name__ == "__main__":
    unittest.main()
