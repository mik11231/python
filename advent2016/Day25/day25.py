#!/usr/bin/env python3
"""Advent of Code 2016 Day 25 Part 1: Clock Signal."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from assembunny import parse_program, run_program


def is_alt(bits: list[int]) -> bool:
    """Return True if bits alternate 0,1,0,1,... from start."""
    return all(b in (0, 1) and b == (i % 2) for i, b in enumerate(bits))


def solve(s: str) -> int:
    """Find smallest a producing alternating clock output prefix."""
    program = parse_program(s)
    a = 0
    while True:
        res = run_program(program, {"a": a, "b": 0, "c": 0, "d": 0}, max_steps=2_000_000, max_output=20)
        if len(res.output) == 20 and is_alt(res.output):
            return a
        a += 1


if __name__ == "__main__":
    text = Path(__file__).with_name("d25_input.txt").read_text(encoding="utf-8")
    print(solve(text))
