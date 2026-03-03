#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 9: Smoke Basin (Part 1)

A heightmap shows the height (0-9) at each position.  A *low point* is
strictly lower than all of its orthogonally adjacent positions.  The risk
level of a low point equals its height plus one.

Algorithm
---------
For each cell, compare with its up/down/left/right neighbors.  If the cell
is strictly less than every existing neighbor it is a low point.  Sum
``height + 1`` for all low points.  O(rows × cols).
"""

from pathlib import Path


def parse_grid(text: str) -> list[list[int]]:
    """Parse a multi-line heightmap into a 2-D list of ints."""
    return [
        [int(ch) for ch in line]
        for line in text.splitlines()
        if line.strip()
    ]


def find_low_points(grid: list[list[int]]) -> list[tuple[int, int, int]]:
    """Return ``(row, col, height)`` for every low point in *grid*."""
    rows, cols = len(grid), len(grid[0])
    low_points: list[tuple[int, int, int]] = []
    for r in range(rows):
        for c in range(cols):
            height = grid[r][c]
            neighbors = []
            if r > 0:
                neighbors.append(grid[r - 1][c])
            if r < rows - 1:
                neighbors.append(grid[r + 1][c])
            if c > 0:
                neighbors.append(grid[r][c - 1])
            if c < cols - 1:
                neighbors.append(grid[r][c + 1])
            if all(height < n for n in neighbors):
                low_points.append((r, c, height))
    return low_points


def solve(input_path: str = "advent2021/Day9/d9_input.txt") -> int:
    """Read the heightmap and return the sum of risk levels of all low points."""
    text = Path(input_path).read_text()
    grid = parse_grid(text)
    return sum(height + 1 for _, _, height in find_low_points(grid))


if __name__ == "__main__":
    result = solve()
    print(f"Sum of risk levels: {result}")
