#!/usr/bin/env python3
"""Advent of Code 2023 Day 6 Part 1 — Wait For It.

For each race, holding the button for t ms in a race of T ms gives
distance t*(T-t). Count how many integer hold-times beat the record
for each race and multiply the counts together. Uses the quadratic
formula for O(1) per race.
"""
import math
from pathlib import Path


def ways_to_win(time: int, record: int) -> int:
    """
    Run `ways_to_win` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: time, record.
    - Returns the computed result for this stage of the pipeline.
    """
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
    times = list(map(int, lines[0].split()[1:]))
    distances = list(map(int, lines[1].split()[1:]))
    result = 1
    for t, d in zip(times, distances):
        result *= ways_to_win(t, d)
    return result


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d6_input.txt").read_text()))
