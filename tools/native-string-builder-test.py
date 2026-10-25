#!/usr/bin/env python3
"""Verify buffered construction, immutable snapshots, aliases and GC ownership."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("binary", type=Path)
parser.add_argument("--reference", type=Path)
args = parser.parse_args()
native = args.binary.resolve()
reference = args.reference.resolve() if args.reference else None
env=dict(os.environ,NO_COLOR='1',TERM='dumb',TRBN_QBE=str(native.with_name("qbe")))
def run(args, data=None, success=True, env=env):
    result = subprocess.run(list(map(str, args)), input=data, env=env,
                            text=True, capture_output=True, timeout=180)
    assert (result.returncode == 0) == success, (args, result.returncode, result.stderr, result.stdout)
    return result

with tempfile.TemporaryDirectory(prefix="native-builder-") as temporary:
    tmp = Path(temporary)
    env["TRBN_HISTORY"] = str(tmp / "history")
    cases = [('boundaries', 'import trb/std/string_builder\n\ndef extend(mut writer: StringBuilder)\n\twriter.append("!")\nend\n\ndef main()\n\tmut writer := StringBuilder.from_string("A")\n\tmut shared := writer\n\twriter.append("\\xf0\\x9f")\n\tputs(writer.size())\n\tearly := writer.to_s()\n\tshared.append("\\x98\\x80")\n\textend(shared)\n\tsnapshot := writer.to_s()\n\tputs(snapshot)\n\tputs(writer.size())\n\tputs(early.to_bytes().size())\n\twriter.clear()\n\tputs(writer.empty?())\n\twriter.append_codepoint(12354)\n\twriter.append_codepoint(0)\n\twriter.append("Z")\n\tputs(writer.size())\n\tputs(writer.to_s().to_bytes().size())\n\tputs(snapshot)\n\tputs(shared.to_s() == writer.to_s())\n\tmut separate := StringBuilder.new()\n\tseparate.append("x")\n\tputs(writer.size())\nend\n', '3\nA😀!\n3\n3\ntrue\n3\n5\nA😀!\ntrue\n3\n'), ('growth', 'import trb/std/string_builder\n\nrecord Held\n\twriter: StringBuilder\n\ttext: String\nend\n\ndef update(mut writer: StringBuilder, count: Integer)\n\tmut i := 0\n\twhile i < count\n\t\twriter.append("a😀")\n\t\ti += 1\n\tend\nend\n\ndef main()\n\tmut writer := StringBuilder.new()\n\tupdate(writer, 1024)\n\tsnapshot := writer.to_s()\n\theld := Held.new(writer: writer, text: snapshot)\n\tmut writers := [writer]\n\tmut shared := writers[0]\n\tupdate(shared, 1024)\n\tputs(held.text.size())\n\tputs(writer.size())\n\tputs(held.writer.to_s().to_bytes().size())\n\twriter.clear()\n\twriter.append("after")\n\tputs(held.text.size())\n\tputs(held.writer.to_s())\n\tmut retained: Array<String> := []\n\tmut i := 0\n\twhile i < 512\n\t\tmut item := StringBuilder.from_string("saved-")\n\t\titem.append(i.to_s())\n\t\tretained.push(item.to_s())\n\t\titem.clear()\n\t\titem.append("changed")\n\t\ti += 1\n\tend\n\tputs(retained[0])\n\tputs(retained[511])\nend\n', '2048\n4096\n10240\n2048\nafter\nsaved-0\nsaved-511\n'), ('display', 'import trb/std/string_builder\ndef show(value: Any)\nputs(value)\nend\ndef main()\nmut writer := StringBuilder.from_string("text")\nputs(writer)\nshow(writer)\nwriter.append("!")\nshow(writer)\nwriter.clear()\nputs(writer.to_s().to_bytes().size())\nputs(writer)\nend\n', 'text\ntext\ntext!\n0\n\n')]
    for name, code, expected in cases:
        source = tmp / (name + ".trb")
        source.write_text(code)
        assert run([native, "check", source]).stdout == "ok\n"
        program = tmp / name
        run([native, "build", "--compile", source, "--outfile", program])
        result = run([program], env=dict(env, TYPE_RB_NATIVE_RUNTIME_STATS="1"))
        assert result.stdout == expected, (name, result.stdout, expected)
        statistics = {line.split(",")[1]: int(line.split(",")[2])
                      for line in result.stderr.splitlines()
                      if line.startswith("type-rb-native-gc-stat-v1,")}
        assert statistics["live-bytes"] == 0
        assert statistics["allocated-bytes"] == statistics["reclaimed-bytes"]
        if reference:
            assert run([reference, "run", source]).stdout == expected
        emitted = run([native, "--internal-driver", "emit-qbe", source]).stdout
        for function in ["trbn_builder_new", "trbn_builder_append",
                         "trbn_builder_append_codepoint", "trbn_builder_to_string"]:
            match = re.search(r"^function(?: l)? \$" + function + r"\([^\n]*\) \{.*?^\}",
                              emitted, re.M | re.S)
            assert match, function
            emitted = emitted.replace(match[0], match[0].replace(
                "@start\n", "@start\n call $trbn_gc_collect(w 0)\n", 1))
        il = tmp / "forced.ssa"
        il.write_text(emitted)
        assembly = tmp / "forced.s"
        run([env["TRBN_QBE"], "-o", assembly, il])
        run(["cc", assembly, "-lm", "-o", tmp / "forced"])
        assert run([tmp / "forced"]).stdout == expected
    # The private span operation is inaccessible to authored source. Alter only
    # one already checked application's call to exercise its defensive bounds.
    source = tmp / "span.trb"
    source.write_text('import trb/std/string_builder\ndef main()\n'
                      'mut writer := StringBuilder.new()\nwriter.append("abc")\nend\n')
    original = run([native, "--internal-driver", "emit-qbe", source]).stdout
    function = next(match for match in re.finditer(
        r"^function[^\n]*\$trbnf[0-9]+\([^\n]*\) \{.*?^\}", original, re.M | re.S)
                    if "call $trbn_builder_append(" in match[0])
    call = re.search(r"call \$trbn_builder_append\((l [^,]+), (l [^)]+)\)", function[0])
    assert call
    for start, finish in [(-1, 2), (0, 4), (2, 1), (0, 9007199254740991)]:
        replacement = f"call $trbn_builder_append_bytes({call[1]}, {call[2]}, l {start}, l {finish})"
        modified = original.replace(function[0], function[0].replace(call[0], replacement))
        il = tmp / "span.ssa"
        il.write_text(modified)
        run([env["TRBN_QBE"], "-o", tmp / "span.s", il])
        run(["cc", tmp / "span.s", "-lm", "-o", tmp / "span"])
        assert "byte range is out of bounds" in run([tmp / "span"], success=False).stderr
    for body in ['writer := StringBuilder.new()\nwriter.append("x")',
                 'mut writer := StringBuilder.new()\nwriter.append(7)',
                 'mut writer := StringBuilder.new()\nwriter.size(1)']:
        source = tmp / "rejected.trb"
        source.write_text("import trb/std/string_builder\ndef main()\n" + body + "\nend\n")
        run([native, "check", source], success=False)
    for point in [-1, 55296, 57343, 1114112]:
        source = tmp / "invalid.trb"
        source.write_text("import trb/std/string_builder\ndef main()\n"
                          "mut writer := StringBuilder.new()\n"
                          f"writer.append_codepoint({point})\nend\n")
        run([native, "build", "--compile", source, "--outfile", tmp / "invalid"])
        result = run([tmp / "invalid"], success=False)
        assert "invalid Unicode code point" in result.stderr
    commands='''import trb/std/string_builder
mut writer := StringBuilder.from_string("A")
mut shared := writer
writer.append("😀")
shared.append_codepoint(33)
writer
writer.size()
snapshot := writer.to_s()
writer.clear()
writer.empty?()
writer.to_s()
writer.append("new")
snapshot
shared.to_s()
:quit
'''
    want='StringBuilder("A") : StringBuilder [mut]\nStringBuilder("A") : StringBuilder [mut]\nStringBuilder("A😀!") : StringBuilder [mut]\n3 : Integer\n"A😀!" : String\ntrue : Boolean\n"" : String\n"A😀!" : String\n"new" : String\n'
    value=run([native,'repl'],data=commands)
    assert value.stdout==want,(value.stdout,want)

print("PASS StringBuilder snapshots, shared mutation, Unicode, growth, GC and retained REPL")
