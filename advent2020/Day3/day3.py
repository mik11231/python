#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 3: Toboggan Trajectory (Part 1)

Starting at the top-left corner of a map that repeats infinitely to the right,
count how many trees ('#') you encounter going right 3, down 1 until you pass
the bottom row.

The map wraps horizontally, so we use modulo arithmetic on the column index
instead of literally duplicating the string.
"""

from pathlib import Path


def count_trees(grid: list[str], right: int = 3, down: int = 1) -> int:
    """Traverse the grid with the given slope and return the number of trees
    encountered.  The grid repeats horizontally via modulo wrapping."""
    col = 0
    trees = 0
    width = len(grid[0])

    for row in range(down, len(grid), down):
        col = (col + right) % width
        if grid[row][col] == "#":
            trees += 1

    return trees


def solve(input_path: str = "advent2020/Day3/d3_input.txt") -> int:
    """Read the map and count trees for slope right-3 down-1."""
    grid = [line for line in Path(input_path).read_text().splitlines() if line.strip()]
    return count_trees(grid)


if __name__ == "__main__":
    result = solve()
    print(f"Trees encountered (right 3, down 1): {result}")
