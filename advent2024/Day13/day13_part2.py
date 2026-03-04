#!/usr/bin/env python3
"""Advent of Code 2024 Day 13 Part 2 - Claw Contraption.

Same linear-algebra approach as Part 1 but with 10^13 added to both prize
coordinates. The 100-press limit no longer applies.
"""
from pathlib import Path
import re

OFFSET = 10_000_000_000_000


def solve(s: str) -> int:
    """Return minimum total tokens with offset prize coordinates."""
    total = 0
    for block in s.strip().split("\n\n"):
        ax, ay, bx, by, px, py = map(int, re.findall(r'\d+', block))
        px += OFFSET
        py += OFFSET
        det = ax * by - ay * bx
        if det == 0:
            continue
        a_num = px * by - py * bx
        b_num = ax * py - ay * px
        if a_num % det or b_num % det:
            continue
        a, b = a_num // det, b_num // det
        if a >= 0 and b >= 0:
            total += 3 * a + b
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d13_input.txt").read_text()))
