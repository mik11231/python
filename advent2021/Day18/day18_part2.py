#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 18: Snailfish (Part 2)

Find the largest magnitude obtainable by adding any two *different*
snailfish numbers from the input.  Order matters (a + b != b + a), so
both orderings of each pair are tested.

Algorithm
---------
Brute-force all ordered pairs (i, j) with i != j.  The ``add`` function
builds new lists from its arguments via list comprehensions, so the
originals are not mutated; however we deep-copy defensively since
``reduce_number`` mutates its list in place.
"""

import copy
from pathlib import Path

from day18 import parse_snailfish, add, magnitude


def solve(input_path: str = "advent2021/Day18/d18_input.txt") -> int:
    """Return the largest magnitude from adding any two different numbers."""
    lines = Path(input_path).read_text().strip().splitlines()
    numbers = [parse_snailfish(line) for line in lines]
    best = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                continue
            result = add(copy.deepcopy(numbers[i]), copy.deepcopy(numbers[j]))
            mag = magnitude(result)
            if mag > best:
                best = mag
    return best


if __name__ == "__main__":
    result = solve()
    print(f"Largest magnitude of any two-number sum: {result}")
