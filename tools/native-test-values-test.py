#!/usr/bin/env python3
"""Check test equality semantics and assertion origins against the pinned oracle."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile


VALUES = '''import { describe, expect, test } from trb/std/test

record Sample
    value: Float
end

class Link
    @value: Float
    @next: Link?
    def initialize(value: Float)
        @value = value
        @next = nil
    end
    def link(following: Link)
        @next = following
    end
end

describe("Equality") do
    test("scalar NaN is unequal to itself") do
        value := 0.0 / 0.0
        expect(value).to_not_equal(value)
    end
    test("signed zero compares by value") do
        expect(0.0).to_equal(-0.0)
    end
    test("same array identity retains the reference shortcut") do
        values := [0.0 / 0.0]
        expect(values).to_equal(values)
        expect(values).to_not_equal([0.0 / 0.0])
    end
    test("same hash identity retains the reference shortcut") do
        values := {"value" => 0.0 / 0.0}
        expect(values).to_equal(values)
        expect(values).to_not_equal({"value" => 0.0 / 0.0})
    end
    test("record storage identity does not bypass field equality") do
        value := Sample.new(value: 0.0 / 0.0)
        expect(value).to_not_equal(value)
    end
    test("class identity and class fields have distinct roles") do
        value := Link.new(0.0 / 0.0)
        expect(value).to_equal(value)
        expect(value).to_not_equal(Link.new(0.0 / 0.0))
        expect(Link.new(4.0)).to_equal(Link.new(4.0))
    end
    test("cycles compare without recurring forever") do
        mut left := Link.new(1.0)
        mut right := Link.new(1.0)
        left.link(left)
        right.link(right)
        expect(left).to_equal(right)
        mut other := Link.new(2.0)
        other.link(other)
        expect(left).to_not_equal(other)
    end
    test("non-nil functions never compare deeply equal") do
        action := fn(): Integer
            return 1
        end
        expect(action).to_not_equal(action)
    end
    test("nullable absence is different from an empty array") do
        absent: Array<Integer>? := nil
        empty: Array<Integer> := []
        expect(absent).to_be_nil()
        expect(empty).to_equal([])
    end
end
'''

ORIGINS = '''import { describe, expect, expect_err, expect_ok, test } from trb/std/test
import trb/std/result

def helper()
    expect(10).to_equal(11)
end

describe("Origins") do
    test("first same-type origin") do
        expect(1).to_equal(2)
    end
    test("second same-type origin") do
        expect(3).to_equal(4)
    end
    test("helper assertion origin") do
        helper()
    end
    test("unicode scalar column") do
        value := "値😀"; expect(value).to_equal("other")
    end
    test("non-Boolean is an assertion failure") do
        expect(1).to_be_true()
    end
    test("wrong Result variant retains the call origin") do
        _value := expect_ok(Result<Integer, String>::Err("bad"))
    end
    test("another Result variant call origin") do
        _value := expect_err(Result<Integer, String>::Ok(1))
    end
    test("runtime trap uses the case origin") do
        values := [1]
        puts(values[3])
    end
    test("later case still runs") do
        expect(true).to_be_true()
    end
end
'''


def replay(binary, root, source, wanted_failures):
    (root / "src/sample_test.trb").write_text(source)
    result = subprocess.run([str(binary), "test", "--reporter", "json"], cwd=root,
                            env=dict(os.environ, NO_COLOR="1", TERM="dumb"),
                            text=True, capture_output=True, timeout=180)
    stdout = result.stdout.replace(str(root), "<project>")
    stderr = result.stderr.replace(str(root), "<project>")
    events = [json.loads(line) for line in stdout.splitlines()]
    assert result.returncode == int(wanted_failures > 0), (result.returncode, stdout, stderr)
    assert len(events) == 19, (stdout, stderr)
    assert events[-1] == {"type": "test_summary", "total": 9, "failed": wanted_failures}, events
    assert sum(event["type"] == "test_failed" for event in events) == wanted_failures, events
    for index in range(0, 18, 2):
        assert events[index]["type"] == "test_started", events[index]
        assert events[index + 1]["type"] in ("test_passed", "test_failed"), events[index + 1]
        assert events[index]["name"] == events[index + 1]["name"], events[index:index + 2]
    assert stderr in ("", "exit status 1\n"), stderr
    return {"code": result.returncode, "events": events, "stderr": stderr,
            "sourceSha256": hashlib.sha256(source.encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--native", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    rows = []
    with tempfile.TemporaryDirectory(prefix="native-test-values-") as directory:
        root = Path(directory)
        (root / "src").mkdir()
        (root / "trbconfig.jsonc").write_text(json.dumps({
            "name": "test-values", "mode": "go", "sourceDir": "src",
            "go": {"module": "example.com/test-values"},
        }) + "\n")
        for name, source, failures in (("values", VALUES, 0), ("origins", ORIGINS, 8)):
            reference = replay(args.reference.resolve(), root, source, failures)
            row = {"id": name, "reference": reference}
            if args.native:
                native = replay(args.native.resolve(), root, source, failures)
                # Different Go wrapper stderr is not a Native runtime obligation.
                assert native["events"] == reference["events"], (name, reference, native)
                row["native"] = native
            rows.append(row)
    report = {"scope": "additional equality and origin controls; historical manifest unchanged",
              "observations": rows}
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"PASS {len(rows)} test-value groups ({'differential' if args.native else 'reference only'})")


if __name__ == "__main__":
    main()
