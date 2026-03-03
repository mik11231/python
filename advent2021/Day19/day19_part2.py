#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 19: Beacon Scanner (Part 2)

Find the largest Manhattan distance between any pair of scanners.

Algorithm
---------
Reuse the scanner alignment from Part 1 to obtain all scanner positions
in the global frame, then compute pairwise Manhattan distances and return
the maximum.
"""

from itertools import combinations
from pathlib import Path

from day19 import parse_scanners, align_scanners


def solve(input_path: str = "advent2021/Day19/d19_input.txt") -> int:
    """Read scanner data, align, and return the max Manhattan distance."""
    text = Path(input_path).read_text()
    scanners = parse_scanners(text)
    _, positions = align_scanners(scanners)
    best = 0
    for (ax, ay, az), (bx, by, bz) in combinations(positions, 2):
        dist = abs(ax - bx) + abs(ay - by) + abs(az - bz)
        if dist > best:
            best = dist
    return best


if __name__ == "__main__":
    result = solve()
    print(f"Largest Manhattan distance between scanners: {result}")
