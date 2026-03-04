#!/usr/bin/env python3
"""Advent of Code 2015 Day 23 Part 2 — Turing Lock with a=1.

Same program, start with a=1, b=0. Return value of b when program terminates.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from day23 import parse_program, run


def solve(s: str) -> int:
    """Return value of register b when program terminates (a=1, b=0)."""
    prog = parse_program(s)
    return run(prog, a=1, b=0)


if __name__ == "__main__":
    text = Path(__file__).with_name("d23_input.txt").read_text(encoding="utf-8")
    print(solve(text))
