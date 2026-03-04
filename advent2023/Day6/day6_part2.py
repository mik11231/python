#!/usr/bin/env python3
"""Advent of Code 2023 Day 6 Part 2 — Wait For It.

Ignore spaces between numbers — there is actually just one long race.
Same quadratic approach as Part 1 but with a single large time and
distance value.
"""
import math
from pathlib import Path


def ways_to_win(time: int, record: int) -> int:
    disc = time * time - 4 * record
    if disc <= 0:
        return 0
    sqrt_disc = math.sqrt(disc)
    lo = (time - sqrt_disc) / 2
    hi = (time + sqrt_disc) / 2
    lo_int = int(math.floor(lo + 1))
    hi_int = int(math.ceil(hi - 1))
    return max(0, hi_int - lo_int + 1)


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    lines = s.strip().splitlines()
    time = int("".join(lines[0].split()[1:]))
    distance = int("".join(lines[1].split()[1:]))
    return ways_to_win(time, distance)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d6_input.txt").read_text()))
