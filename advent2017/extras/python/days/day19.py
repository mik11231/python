#!/usr/bin/env python3
"""AoC 2017 Day 19 fancy Python implementation (tube tracer)."""

from __future__ import annotations

import argparse
import hashlib
import string
import time
from pathlib import Path

EXPECTED_SHA256 = "b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a"
EXPECTED_PART1 = "DTOUFARJQ"
EXPECTED_PART2 = "16642"


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
        Path("advent2017/Day19/d19_input.txt"),
        Path("Day19/d19_input.txt"),
        Path("../Day19/d19_input.txt"),
        Path("../../Day19/d19_input.txt"),
        Path(__file__).resolve().parents[2] / "Day19" / "d19_input.txt",
    ]
    for c in cands:
        if c.exists():
            return c.resolve()
    raise FileNotFoundError("input not found for day 19")


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


def parse_grid(raw: str) -> list[list[str]]:
    """
    Run `parse_grid` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    lines = raw.splitlines()
    w = max(len(line) for line in lines)
    return [list(line.ljust(w, " ")) for line in lines]


def at(grid: list[list[str]], r: int, c: int) -> str:
    """
    Run `at` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid, r, c.
    - Returns the computed result for this stage of the pipeline.
    """
    if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]):
        return " "
    return grid[r][c]


def solve(raw: str) -> tuple[str, int]:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: raw.
    - Returns the computed result for this stage of the pipeline.
    """
    g = parse_grid(raw)
    r, c = 0, g[0].index("|")
    dr, dc = 1, 0
    letters: list[str] = []
    steps = 0

    while True:
        ch = at(g, r, c)
        if ch == " ":
            break
        if ch in string.ascii_uppercase:
            letters.append(ch)
        elif ch == "+":
            if dr != 0:
                if at(g, r, c - 1) != " ":
                    dr, dc = 0, -1
                elif at(g, r, c + 1) != " ":
                    dr, dc = 0, 1
            else:
                if at(g, r - 1, c) != " ":
                    dr, dc = -1, 0
                elif at(g, r + 1, c) != " ":
                    dr, dc = 1, 0
        r += dr
        c += dc
        steps += 1

    return "".join(letters), steps


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
    ap = argparse.ArgumentParser(description="AoC 2017 Day 19 fancy Python")
    ap.add_argument("--part", type=int, required=True, choices=[1, 2])
    ap.add_argument("--input")
    args = ap.parse_args()

    input_path = Path(args.input).resolve() if args.input else default_input_path()
    got_sha = sha256_file(input_path)
    if got_sha != EXPECTED_SHA256:
        raise SystemExit(f"checksum mismatch: {got_sha} != {EXPECTED_SHA256}")

    t0 = time.perf_counter_ns()
    p1, p2 = solve(input_path.read_text(encoding="utf-8"))
    answer = p1 if args.part == 1 else str(p2)
    runtime_ms = (time.perf_counter_ns() - t0) / 1e6

    expected = EXPECTED_PART1 if args.part == 1 else EXPECTED_PART2
    if answer != expected:
        raise SystemExit(f"answer mismatch for part {args.part}: got {answer!r}, expected {expected!r}")

    print(answer)
    print(f"[python-fancy] day=19 part={args.part} runtime_ms={runtime_ms:.3f}", file=__import__("sys").stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
