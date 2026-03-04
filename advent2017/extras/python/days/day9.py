#!/usr/bin/env python3
"""AoC 2017 Day 9 fancy Python implementation (real algorithms for both parts)."""

from __future__ import annotations

import argparse
import hashlib
import time
from pathlib import Path

EXPECTED_SHA256 = "860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3"
EXPECTED_PART1 = "21037"
EXPECTED_PART2 = "9495"


def default_input_path() -> Path:
    """
    Run `default_input_path` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    cands = [
        Path("advent2017/Day9/d9_input.txt"),
        Path("Day9/d9_input.txt"),
        Path("../Day9/d9_input.txt"),
        Path("../../Day9/d9_input.txt"),
        Path(__file__).resolve().parents[2] / "Day9" / "d9_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 9")


def sha256_file(path: Path) -> str:
    """
    Run `sha256_file` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_stream(raw: str) -> tuple[int, int]:
    """
    Run `scan_stream` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    t = raw.strip()
    depth = 0
    score = 0
    garbage_count = 0
    in_garbage = False
    i = 0

    while i < len(t):
        c = t[i]
        if in_garbage:
            if c == "!":
                i += 2
                continue
            if c == ">":
                in_garbage = False
            else:
                garbage_count += 1
        else:
            if c == "<":
                in_garbage = True
            elif c == "{":
                depth += 1
                score += depth
            elif c == "}":
                depth -= 1
        i += 1

    return score, garbage_count


def main() -> int:
    """
    Run `main` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Returns the computed result for this stage of the pipeline.
    """
    ap = argparse.ArgumentParser(description="AoC 2017 Day 9 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    raw = input_path.read_text(encoding="utf-8")

    t0 = time.perf_counter_ns()
    p1, p2 = scan_stream(raw)
    answer = str(p1 if args.part == 1 else p2)
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=9 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
