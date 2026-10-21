"""Check exported snapshot bytes against the recovery decoder's own bound."""

from pathlib import Path
import re
import sys


def compiler_input_limit(decoder: Path) -> int:
    matches = re.findall(
        r"^COMPILER_RECOVERY_MAX_INPUT_BYTES := ([0-9]+)$",
        decoder.read_text(encoding="utf-8"),
        re.MULTILINE,
    )
    if len(matches) != 1 or int(matches[0]) <= 0:
        raise ValueError("expected one positive compiler recovery byte limit")
    return int(matches[0])


def check_size(snapshot: Path, decoder: Path) -> tuple[int, int]:
    limit = compiler_input_limit(decoder)
    size = snapshot.stat().st_size
    if size == 0 or size > limit:
        raise ValueError(f"compiler recovery snapshot has {size} bytes; expected 1..{limit}")
    return size, limit


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: bootstrap_snapshot_size.py SNAPSHOT", file=sys.stderr)
        return 2
    decoder = Path(__file__).resolve().parent.parent / "recovery/src/managed/snapshot.trb"
    try:
        size, limit = check_size(Path(sys.argv[1]), decoder)
    except (OSError, ValueError) as error:
        print(f"bootstrap snapshot: {error}", file=sys.stderr)
        return 1
    print(f"bootstrap snapshot: {size} bytes / {limit} byte input limit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
