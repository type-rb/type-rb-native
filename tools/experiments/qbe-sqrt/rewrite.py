"""Diagnostic ablation of canonical typed sqrt calls in accepted Native QBE.

This is not a production optimizer. The caller must provide QBE emitted by the
accepted compiler from the fixed public inputs and audit the occurrence count.
"""
import argparse
import json
import re
from pathlib import Path

PATTERN = re.compile(r"^(\s*%[A-Za-z0-9_.]+ =d )call \$sqrt\(d ([^()\n]+)\)$", re.M)


def rewrite(source):
    result, count = PATTERN.subn(r"\1sqrt \2", source)
    if "call $sqrt(" in result:
        raise ValueError("unrecognized sqrt call; refusing partial substitution")
    return result, count


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--count", type=int, required=True)
    args = p.parse_args()
    result, count = rewrite(args.source.read_text())
    if count != args.count:
        raise ValueError(f"expected {args.count} canonical calls, found {count}")
    args.output.write_text(result)
    print(json.dumps({"transformedCalls": count}))
