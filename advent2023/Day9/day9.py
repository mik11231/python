#!/usr/bin/env python3
"""Advent of Code 2023 Day 9 Part 1 — Mirage Maintenance.

For each history, repeatedly compute differences until all zeros, then
extrapolate the next value by summing the last elements of each layer.
Return the sum of all extrapolated next values.
"""
from pathlib import Path


def extrapolate_next(seq: list[int]) -> int:
    """Return the next value in the sequence."""
    lasts: list[int] = []
    while any(v != 0 for v in seq):
        lasts.append(seq[-1])
        seq = [b - a for a, b in zip(seq, seq[1:])]
    return sum(lasts)


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    return sum(
        extrapolate_next(list(map(int, line.split())))
        for line in s.strip().splitlines()
    )


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d9_input.txt").read_text()))
