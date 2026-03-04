#!/usr/bin/env python3
"""Advent of Code 2023 Day 13 Part 2 — Point of Incidence.

Same as Part 1, but find the reflection line with exactly 1 smudge
(one cell that, if flipped, would make the reflection perfect).
"""
from pathlib import Path
from day13 import find_reflection


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    return sum(
        find_reflection(block.splitlines(), target_smudges=1)
        for block in s.strip().split("\n\n")
    )


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d13_input.txt").read_text()))
