#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 11: Dumbo Octopus (Part 2)

Find the first step during which all 100 octopuses flash simultaneously.

Algorithm
---------
Reuse the ``step`` function from Part 1.  Keep stepping until the flash
count for a single step equals the grid size (rows × cols).
"""

from pathlib import Path

from day11 import parse_grid, step


def solve(input_path: str = "advent2021/Day11/d11_input.txt") -> int:
    """Read the octopus grid and return the first step where all flash."""
    text = Path(input_path).read_text()
    grid = parse_grid(text)
    total_cells = len(grid) * len(grid[0])
    step_num = 0
    while True:
        step_num += 1
        if step(grid) == total_cells:
            return step_num


if __name__ == "__main__":
    result = solve()
    print(f"First step where all octopuses flash: {result}")
