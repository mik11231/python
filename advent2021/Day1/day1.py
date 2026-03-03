#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 1: Sonar Sweep (Part 1)

A submarine's sonar sweep reports a series of sea-floor depth measurements.
Count how many measurements are *larger* than the previous measurement.

Algorithm
---------
Single pass comparing each element to its predecessor via ``zip``, giving
O(n) time and O(1) extra space.
"""

from pathlib import Path


def count_increases(depths: list[int]) -> int:
    """Return the number of times a depth measurement increases."""
    return sum(b > a for a, b in zip(depths, depths[1:]))


def solve(input_path: str = "advent2021/Day1/d1_input.txt") -> int:
    """Read depth measurements and return the increase count."""
    depths = [
        int(line)
        for line in Path(input_path).read_text().splitlines()
        if line.strip()
    ]
    return count_increases(depths)


if __name__ == "__main__":
    result = solve()
    print(f"Number of depth increases: {result}")
