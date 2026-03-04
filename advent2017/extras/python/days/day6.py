#!/usr/bin/env python3
"""AoC 2017 Day 6 fancy Python implementation (real algorithms for both parts)."""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA256 = "489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba"
EXPECTED_PART1 = "12841"
EXPECTED_PART2 = "8038"


def default_input_path() -> Path:
    cands = [
        Path("advent2017/Day6/d6_input.txt"),
        Path("Day6/d6_input.txt"),
        Path("../Day6/d6_input.txt"),
        Path("../../Day6/d6_input.txt"),
        Path(__file__).resolve().parents[2] / "Day6" / "d6_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 6")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_banks(raw: str) -> list[int]:
    return [int(x) for x in raw.split()]


def redistribute(a: list[int]) -> None:
    i = max(range(len(a)), key=lambda k: (a[k], -k))
    blocks = a[i]
    a[i] = 0
    n = len(a)
    q, r = divmod(blocks, n)
    if q:
        for k in range(n):
            a[k] += q
    for t in range(1, r + 1):
        a[(i + t) % n] += 1


def solve_part1(banks: list[int]) -> int:
    a = banks[:]
    seen: set[tuple[int, ...]] = set()
    steps = 0
    while tuple(a) not in seen:
        seen.add(tuple(a))
        redistribute(a)
        steps += 1
    return steps


def solve_part2(banks: list[int]) -> int:
    a = banks[:]
    seen: dict[tuple[int, ...], int] = {}
    steps = 0
    while tuple(a) not in seen:
        seen[tuple(a)] = steps
        redistribute(a)
        steps += 1
    return steps - seen[tuple(a)]


def main() -> int:
    ap = argparse.ArgumentParser(description="AoC 2017 Day 6 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    banks = parse_banks(input_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    answer = str(solve_part1(banks) if args.part == 1 else solve_part2(banks))
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=6 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
