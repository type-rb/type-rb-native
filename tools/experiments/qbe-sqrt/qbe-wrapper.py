#!/usr/bin/env python3
"""Capture accepted Native QBE and apply the registered backend-only ablation."""
import json
import os
import sys
from pathlib import Path
from rewrite import rewrite

source = Path(sys.argv[-1])
assert source.is_file()
prefix = Path(os.environ["SQRT_EVIDENCE_PREFIX"])
original = source.read_text()
prefix.with_suffix(".original.ssa").write_text(original)
result, count = rewrite(original)
assert count == int(os.environ["SQRT_EXPECTED_CALLS"]), count
mode = os.environ["SQRT_MODE"]
assert mode in ("upstream", "candidate")
if mode == "candidate":
    source.write_text(result)
prefix.with_suffix(".ssa").write_text(source.read_text())
prefix.with_suffix(".json").write_text(json.dumps({"mode": mode, "calls": count}) + "\n")
backend = os.environ["SQRT_QBE"]
os.execv(backend, [backend, *sys.argv[1:]])
