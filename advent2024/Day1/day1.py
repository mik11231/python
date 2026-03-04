#!/usr/bin/env python3
"""Advent of Code 2024 Day 1 Part 1 — Historian Hysteria.

Parse two columns of location IDs, sort each independently, then sum the
absolute differences of each paired element. The answer is the total distance.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Sort both lists and return the sum of pairwise absolute differences."""
    left, right = [], []
    for line in s.strip().splitlines():
        a, b = line.split()
        left.append(int(a))
        right.append(int(b))
    left.sort()
    right.sort()
    return sum(abs(a - b) for a, b in zip(left, right))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d1_input.txt").read_text()))
