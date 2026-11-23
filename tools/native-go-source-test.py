#!/usr/bin/env python3
"""Verify scalar Go source output and CLI execution on ordinary projects."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile


native = Path(sys.argv[1]).resolve()


def run(command, cwd, *, check=True):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=60)
    if check:
        assert result.returncode == 0, result
    return result


with tempfile.TemporaryDirectory(prefix="native-go-source-") as temporary:
    root = Path(temporary)
    project = root / "go project"
    source = project / "src"
    source.mkdir(parents=True)
    (project / "trbconfig.jsonc").write_text(json.dumps({
        "name": "source-check",
        "mode": "go",
        "sourceDir": "src",
        "outDir": "build",
        "packageManagement": "external",
        "go": {"module": "example.com/source-check", "version": "1.27"},
    }))
    (source / "totals.trb").write_text(
        "def sum(left: Integer, right: Integer): Integer\n"
        "    return left + right\nend\n"
    )
    main = source / "main.trb"
    main.write_text(
        "import { sum } from totals\n\n"
        "def main()\n    puts(sum(40, 2))\nend\n"
    )
    assert run([native, "check"], project).stdout == "ok\n"
    generated = run([native, "build", "--stdout"], project).stdout
    assert generated.startswith("package main\n")
    assert not (project / "build").exists()
    go_source = root / "main.go"
    go_source.write_text(generated)
    assert run(["go", "run", go_source], root).stdout == "42\n"
    assert run([native, "run"], project).stdout == "42\n"
    run([native, "build"], project)
    generated_module = project / "build" / "trb"
    assert "example.com/source-check" in (generated_module / "go.mod").read_text()
    assert run(["go", "run", "."], generated_module).stdout == "42\n"
    extra = project / "build" / "keep.txt"
    extra.write_text("unrelated output")
    run([native, "build"], project)
    assert extra.read_text() == "unrelated output"
    assert run(["go", "run", "."], generated_module).stdout == "42\n"

    destination = project / "bin with spaces" / "program"
    run([native, "build", "--compile", "--outfile", destination], project)
    assert run([destination], project).stdout == "42\n"
    original_binary = destination.read_bytes()
    main.write_text("def main()\n    puts(missing)\nend\n")
    failure = run([native, "build", "--compile", "--outfile", destination], project, check=False)
    assert failure.returncode == 1 and "main.trb:2:" in failure.stderr, failure
    assert destination.read_bytes() == original_binary

    control = root / "control.trb"
    control.write_text(
        "def main()\n"
        "    mut total := 0\n"
        "    while total < 41\n"
        "        total += 1\n"
        "    end\n"
        "    if total == 41\n"
        "        puts(total + 1)\n"
        "    end\n"
        "end\n"
    )
    assert run([native, "run", "--mode", "go", control], root).stdout == "42\n"

    standalone = root / "standalone.trb"
    standalone.write_text('def main()\n    puts("日本語")\n    puts(true)\nend\n')
    result = run([native, "run", "--mode", "go", standalone], root)
    assert result.stdout == "日本語\ntrue\n", result
