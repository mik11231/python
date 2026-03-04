#!/usr/bin/env python3
"""Advent of Code 2015 Day 11 Part 2 — Next valid after Part 1 answer."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day11 import next_valid, solve as solve_part1


def solve(s: str) -> str:
    """Return next valid password after the Part 1 answer (for same input)."""
    part1_answer = solve_part1(s)
    return next_valid(part1_answer)


if __name__ == "__main__":
    text = Path(__file__).with_name("d11_input.txt").read_text(encoding="utf-8")
    print(solve(text))
