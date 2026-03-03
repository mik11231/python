#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 3: Toboggan Trajectory (Part 2)

Check several slopes and multiply the tree counts together.

Slopes to check:
    Right 1, Down 1
    Right 3, Down 1
    Right 5, Down 1
    Right 7, Down 1
    Right 1, Down 2
"""

import math
from pathlib import Path

from day3 import count_trees

SLOPES = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2),
]


def solve(input_path: str = "advent2020/Day3/d3_input.txt") -> int:
    """Read the map, count trees for every slope, return the product."""
    grid = [line for line in Path(input_path).read_text().splitlines() if line.strip()]
    counts = [count_trees(grid, right, down) for right, down in SLOPES]
    return math.prod(counts)


if __name__ == "__main__":
    result = solve()
    print(f"Product of tree counts across all slopes: {result}")
