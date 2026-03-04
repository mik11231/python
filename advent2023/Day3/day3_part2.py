#!/usr/bin/env python3
"""Advent of Code 2023 Day 3 Part 2 — Gear Ratios.

A gear is any '*' symbol adjacent to exactly two part numbers.
Its gear ratio is the product of those two numbers. Return the sum
of all gear ratios in the schematic.
"""
import re
from collections import defaultdict
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    star_numbers: dict[tuple[int, int], list[int]] = defaultdict(list)

    for r, row in enumerate(grid):
        for m in re.finditer(r"\d+", row):
            num = int(m.group())
            seen_stars: set[tuple[int, int]] = set()
            for dr in (-1, 0, 1):
                for c in range(m.start() - 1, m.end() + 1):
                    nr = r + dr
                    if 0 <= nr < rows and 0 <= c < cols and grid[nr][c] == "*":
                        seen_stars.add((nr, c))
            for star in seen_stars:
                star_numbers[star].append(num)

    return sum(nums[0] * nums[1] for nums in star_numbers.values() if len(nums) == 2)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d3_input.txt").read_text()))
