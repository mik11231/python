#!/usr/bin/env python3
"""AoC 2017 Day 10 fancy Python implementation (real knot-hash algorithms)."""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA256 = "b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69"
EXPECTED_PART1 = "54675"
EXPECTED_PART2 = "a7af2706aa9a09cf5d848c1e6605dd2a"
SUFFIX = [17, 31, 73, 47, 23]


def default_input_path() -> Path:
    cands = [
        Path("advent2017/Day10/d10_input.txt"),
        Path("Day10/d10_input.txt"),
        Path("../Day10/d10_input.txt"),
        Path("../../Day10/d10_input.txt"),
        Path(__file__).resolve().parents[2] / "Day10" / "d10_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 10")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def reverse_segment(a: list[int], start: int, length: int) -> None:
    n = len(a)
    for i in range(length // 2):
        x = (start + i) % n
        y = (start + length - 1 - i) % n
        a[x], a[y] = a[y], a[x]


def run_round(a: list[int], lengths: list[int], pos: int, skip: int) -> tuple[int, int]:
    n = len(a)
    for length in lengths:
        reverse_segment(a, pos, length)
        pos = (pos + length + skip) % n
        skip += 1
    return pos, skip


def solve_part1(raw: str) -> int:
    lengths = [int(x) for x in raw.strip().split(",") if x.strip()]
    ring = list(range(256))
    run_round(ring, lengths, 0, 0)
    return ring[0] * ring[1]


def solve_part2(raw: str) -> str:
    lengths = [ord(c) for c in raw.strip()] + SUFFIX
    ring = list(range(256))
    pos = 0
    skip = 0
    for _ in range(64):
        pos, skip = run_round(ring, lengths, pos, skip)

    dense: list[int] = []
    for block in range(16):
        x = 0
        for v in ring[block * 16 : (block + 1) * 16]:
            x ^= v
        dense.append(x)
    return "".join(f"{x:02x}" for x in dense)


def main() -> int:
    ap = argparse.ArgumentParser(description="AoC 2017 Day 10 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    raw = input_path.read_text(encoding="utf-8")

    t0 = time.perf_counter_ns()
    answer = str(solve_part1(raw)) if args.part == 1 else solve_part2(raw)
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=10 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
