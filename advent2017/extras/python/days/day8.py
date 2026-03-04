#!/usr/bin/env python3
"""AoC 2017 Day 8 fancy Python implementation (real algorithms for both parts)."""

from __future__ import annotations

import argparse
import hashlib
import operator
import time
from collections import defaultdict
from pathlib import Path

EXPECTED_SHA256 = "a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd"
EXPECTED_PART1 = "5143"
EXPECTED_PART2 = "6209"
OPS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}


def default_input_path() -> Path:
    cands = [
        Path("advent2017/Day8/d8_input.txt"),
        Path("Day8/d8_input.txt"),
        Path("../Day8/d8_input.txt"),
        Path("../../Day8/d8_input.txt"),
        Path(__file__).resolve().parents[2] / "Day8" / "d8_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_program(raw: str) -> tuple[int, int]:
    reg: defaultdict[str, int] = defaultdict(int)
    peak = 0

    for line in raw.splitlines():
        if not line.strip():
            continue
        r, op, v, _, cr, cmpop, cv = line.split()
        if OPS[cmpop](reg[cr], int(cv)):
            reg[r] += int(v) if op == "inc" else -int(v)
            peak = max(peak, reg[r])

    return (max(reg.values()) if reg else 0), peak


def main() -> int:
    ap = argparse.ArgumentParser(description="AoC 2017 Day 8 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    raw = input_path.read_text(encoding="utf-8")

    t0 = time.perf_counter_ns()
    p1, p2 = run_program(raw)
    answer = str(p1 if args.part == 1 else p2)
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=8 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
