import copy
import json
from pathlib import Path
import tempfile
import unittest

from backends import BackendRoles, digest, validate_observations


class BackendRoutingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.compilers = {role: {"path": str(self.root / role / "compiler")}
                          for role in ("native", "previous", "baseline")}
        self.paths, self.expected = {}, {}
        for role in ("native", "previous"):
            path = self.root / (role + "-qbe") / "qbe"
            path.parent.mkdir()
            path.write_bytes(role.encode())
            inputs = dict(backend={"variant": role}, builderSHA256="a" * 64,
                          ccSHA256="b" * 64, platform="linux", machine="aarch64")
            receipt = dict(inputs=inputs, binarySHA256=digest(path))
            path.with_name("build-info.json").write_text(json.dumps(receipt))
            self.paths[role] = path
            self.expected[role] = dict(backend=inputs["backend"], builderSha256=inputs["builderSHA256"])
        self.expected["baseline"] = copy.deepcopy(self.expected["previous"])

    def router(self):
        return BackendRoles(self.compilers, self.paths["native"], self.paths["previous"], self.expected)

    def command(self, role):
        return [self.compilers[role]["path"], "build", "source.trb", "--output", "program",
                "--qbe", str(self.paths["native"]), "--cc", "/usr/bin/cc"]

    def test_only_backend_argument_changes_for_each_native_role(self):
        router = self.router()
        for role in self.compilers:
            original = self.command(role)
            expected = list(original)
            expected[6] = str(self.paths["native" if role == "native" else "previous"])
            self.assertEqual(router.route(original), expected)
            self.assertEqual(original, self.command(role))
        for command in [["program", "12"], ["go", "build", "main.go"],
                        [self.compilers["native"]["path"], "emit-qbe", "source.trb"]]:
            self.assertEqual(router.route(command), command)

    def test_unknown_compiler_and_altered_backend_arguments_fail_closed(self):
        router = self.router()
        for command in [["unknown", *self.command("native")[1:]],
                        self.command("native") + ["--qbe", str(self.paths["native"])],
                        [self.compilers["native"]["path"], "run", *self.command("native")[2:]]]:
            with self.assertRaises(ValueError):
                router.route(command)
        altered = self.command("native")
        altered[6] = str(self.paths["previous"])
        with self.assertRaises(ValueError):
            router.route(altered)

    def test_receipt_and_post_collection_binary_changes_are_rejected(self):
        router = self.router()
        router.verify_unchanged()
        self.paths["native"].write_bytes(b"different")
        with self.assertRaises(ValueError):
            router.verify_unchanged()
        with self.assertRaises(ValueError):
            self.router()

    def test_registered_builder_and_backend_are_required(self):
        for field, value in [("builderSha256", "f" * 64), ("backend", {"variant": "wrong"})]:
            expected = copy.deepcopy(self.expected)
            expected["native"][field] = value
            with self.assertRaises(ValueError):
                BackendRoles(self.compilers, self.paths["native"], self.paths["previous"], expected)

    def test_independent_command_audit_detects_wrong_role_backend(self):
        router = self.router()
        records = [dict(role=role, kind="build", command=router.route(self.command(role)))
                   for role in self.compilers]
        validate_observations(records, router.identities, self.expected)
        changed = copy.deepcopy(records)
        changed[1]["command"][6] = str(self.paths["native"])
        with self.assertRaises(ValueError):
            validate_observations(changed, router.identities, self.expected)


if __name__ == "__main__":
    unittest.main()
