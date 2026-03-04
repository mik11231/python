#!/usr/bin/env python3
"""Advent of Code 2024 Day 13 Part 1 - Claw Contraption.

Each claw machine is a 2x2 linear system: a*Ax + b*Bx = Px, a*Ay + b*By = Py.
Solve via Cramer's rule; if the unique solution is non-negative integers with
a,b <= 100, the cost is 3a + b. Sum costs of all winnable machines.
"""
from pathlib import Path
import re


def solve(s: str) -> int:
    """Return minimum total tokens to win all possible prizes."""
    total = 0
    for block in s.strip().split("\n\n"):
        ax, ay, bx, by, px, py = map(int, re.findall(r'\d+', block))
        det = ax * by - ay * bx
        if det == 0:
            continue
        a_num = px * by - py * bx
        b_num = ax * py - ay * px
        if a_num % det or b_num % det:
            continue
        a, b = a_num // det, b_num // det
        if 0 <= a <= 100 and 0 <= b <= 100:
            total += 3 * a + b
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d13_input.txt").read_text()))
