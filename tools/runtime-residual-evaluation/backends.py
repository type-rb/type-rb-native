"""Bind each Native compiler role to its registered QBE build and receipt."""
import hashlib
import json
from pathlib import Path
import re

NATIVE_ROLES = ("native", "previous", "baseline")
DIGEST = re.compile(r"[0-9a-f]{64}")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class BackendRoles:
    def __init__(self, compilers, current, previous, expected):
        if set(expected) != set(NATIVE_ROLES):
            raise ValueError("Missing registered backend role")
        paths = {"native": Path(current).resolve(),
                 "previous": Path(previous).resolve(),
                 "baseline": Path(previous).resolve()}
        self.by_compiler = {str(Path(compilers[role]["path"]).resolve()): role
                            for role in NATIVE_ROLES}
        if len(self.by_compiler) != len(NATIVE_ROLES):
            raise ValueError("Compiler roles must have distinct paths")
        self.placeholder = str(Path(current).resolve())
        self.identities = {}
        for role, path in paths.items():
            receipt_path = path.with_name("build-info.json")
            receipt = json.loads(receipt_path.read_text())
            inputs = receipt["inputs"]
            sha = digest(path)
            if (receipt["binarySHA256"] != sha or
                    inputs["backend"] != expected[role]["backend"] or
                    inputs["builderSHA256"] != expected[role]["builderSha256"] or
                    inputs["platform"] != "linux" or inputs["machine"] != "aarch64" or
                    not DIGEST.fullmatch(inputs["ccSHA256"])):
                raise ValueError("Backend receipt differs for " + role)
            self.identities[role] = {"path": str(path), "sha256": sha,
                                     "bytes": path.stat().st_size,
                                     "receiptPath": str(receipt_path),
                                     "receiptSha256": digest(receipt_path),
                                     "inputs": inputs}
        if (self.identities["native"]["sha256"] == self.identities["previous"]["sha256"] or
                len({row["inputs"]["ccSHA256"] for row in self.identities.values()}) != 1):
            raise ValueError("Backend change or matching C compiler is unproven")

    def for_role(self, role):
        return self.identities[role]["path"]

    def route(self, command):
        """Change only the registered Native build's backend argument."""
        command = list(map(str, command))
        if "--qbe" not in command:
            return command
        role = self.by_compiler.get(str(Path(command[0]).resolve()))
        if (role is None or len(command) < 2 or command[1] != "build" or
                command.count("--qbe") != 1):
            raise ValueError("Unknown compiler invocation with a backend")
        position = command.index("--qbe") + 1
        if position >= len(command) or str(Path(command[position]).resolve()) != self.placeholder:
            raise ValueError("Unexpected initial backend argument")
        command[position] = self.for_role(role)
        return command

    def verify_unchanged(self):
        for role, row in self.identities.items():
            if digest(row["path"]) != row["sha256"] or digest(row["receiptPath"]) != row["receiptSha256"]:
                raise ValueError("Backend changed during comparison: " + role)


def validate_observations(records, identities, expected):
    """Audit actual timed commands, independently of the routing adapter."""
    if set(identities) != set(NATIVE_ROLES):
        raise ValueError("Incomplete backend identities")
    for role in NATIVE_ROLES:
        row = identities[role]
        if (not DIGEST.fullmatch(row["sha256"]) or row["bytes"] <= 0 or
                row["inputs"]["backend"] != expected[role]["backend"] or
                row["inputs"]["builderSHA256"] != expected[role]["builderSha256"]):
            raise ValueError("Backend identity disagrees with registration")
    for row in records:
        command = list(map(str, row["command"]))
        if row["role"] not in NATIVE_ROLES or row["kind"] not in ("build", "compiler-self", "compiler-cost"):
            if "--qbe" in command:
                raise ValueError("Unexpected backend on a non-build observation")
            continue
        if (command.count("--qbe") != 1 or command.index("--qbe") + 1 >= len(command) or
                command[command.index("--qbe") + 1] != identities[row["role"]]["path"]):
            raise ValueError("Timed build used a different backend")
