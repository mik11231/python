#!/usr/bin/env python3
"""AoC 2017 Day 1 fancy Python implementation (real algorithm, both parts)."""

from __future__ import annotations

import argparse
import hashlib
import time
from dataclasses import dataclass
from pathlib import Path

DAY = 1
EXPECTED_SHA256 = "ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef"
EXPECTED_PART1 = "1158"
EXPECTED_PART2 = "1132"


@dataclass(frozen=True)
class CaptchaInput:
    """Normalized input representation for fast digit comparisons."""

    digits: bytes

    @staticmethod
    def from_text(raw: str) -> "CaptchaInput":
        # AoC input is a single line of ASCII digits. We strip surrounding
        # whitespace once and keep bytes for tight-loop integer operations.
        cleaned = raw.strip().encode("ascii")
        if not cleaned:
            raise ValueError("empty captcha input")
        if any(ch < 48 or ch > 57 for ch in cleaned):
            raise ValueError("captcha input must contain only digits")
        return CaptchaInput(digits=cleaned)


def default_input_path() -> Path:
    """Resolve input path from common working directories."""
    cands = [
        Path("advent2017/Day1/d1_input.txt"),
        Path("Day1/d1_input.txt"),
        Path("../Day1/d1_input.txt"),
        Path("../../Day1/d1_input.txt"),
        Path(__file__).resolve().parents[2] / "Day1" / "d1_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 1")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def solve_part1(inp: CaptchaInput) -> int:
    """Compute inverse-captcha sum for adjacent circular matches."""
    data = inp.digits
    n = len(data)
    total = 0
    for i, cur in enumerate(data):
        nxt = data[(i + 1) % n]
        if cur == nxt:
            total += cur - 48  # ASCII '0' -> 48
    return total


def solve_part2(inp: CaptchaInput) -> int:
    """Compute inverse-captcha sum for halfway-around circular matches."""
    data = inp.digits
    n = len(data)
    step = n // 2
    total = 0
    for i, cur in enumerate(data):
        nxt = data[(i + step) % n]
        if cur == nxt:
            total += cur - 48
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="AoC 2017 Day 1 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    raw = input_path.read_text(encoding="utf-8")
    parsed = CaptchaInput.from_text(raw)

    t0 = time.perf_counter_ns()
    if args.part == 1:
        answer = str(solve_part1(parsed))
        expected = EXPECTED_PART1
    else:
        answer = str(solve_part2(parsed))
        expected = EXPECTED_PART2
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(
        f"[python-fancy] day=1 part={args.part} runtime_ms={runtime_ms:.3f}",
        file=__import__("sys").stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
