#!/usr/bin/env python3
"""Advent of Code 2023 Day 9 Part 2 — Mirage Maintenance.

Same difference-sequence approach, but extrapolate backwards.  Collect the
first elements of each layer, then fold from the bottom: prev = first - prev.
"""
from pathlib import Path
from functools import reduce


def extrapolate_prev(seq: list[int]) -> int:
    """Return the previous (leftward) value in the sequence."""
    firsts: list[int] = []
    while any(v != 0 for v in seq):
        firsts.append(seq[0])
        seq = [b - a for a, b in zip(seq, seq[1:])]
    return reduce(lambda acc, x: x - acc, reversed(firsts), 0)


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    return sum(
        extrapolate_prev(list(map(int, line.split())))
        for line in s.strip().splitlines()
    )


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d9_input.txt").read_text()))
