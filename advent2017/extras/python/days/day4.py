#!/usr/bin/env python3
"""AoC 2017 Day 4 fancy Python implementation (real algorithms for both parts)."""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA256 = "36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401"
EXPECTED_PART1 = "451"
EXPECTED_PART2 = "223"


def default_input_path() -> Path:
    cands = [
        Path("advent2017/Day4/d4_input.txt"),
        Path("Day4/d4_input.txt"),
        Path("../Day4/d4_input.txt"),
        Path("../../Day4/d4_input.txt"),
        Path(__file__).resolve().parents[2] / "Day4" / "d4_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 4")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_lines(raw: str) -> list[list[str]]:
    return [line.split() for line in raw.splitlines() if line.strip()]


def solve_part1(lines: list[list[str]]) -> int:
    # A passphrase is valid when all words are distinct.
    return sum(1 for words in lines if len(words) == len(set(words)))


def solve_part2(lines: list[list[str]]) -> int:
    # Normalize each word by sorted letters, then require uniqueness.
    total = 0
    for words in lines:
        canon = ["".join(sorted(w)) for w in words]
        total += int(len(canon) == len(set(canon)))
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="AoC 2017 Day 4 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    lines = parse_lines(input_path.read_text(encoding="utf-8"))

    t0 = time.perf_counter_ns()
    if args.part == 1:
        answer = str(solve_part1(lines))
        expected = EXPECTED_PART1
    else:
        answer = str(solve_part2(lines))
        expected = EXPECTED_PART2
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=4 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
