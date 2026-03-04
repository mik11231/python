#!/usr/bin/env python3
"""Advent of Code 2024 Day 4 Part 2 — Ceres Search (X-MAS).

Find X-shaped MAS patterns: the center cell is 'A', and each of the two
diagonals (top-left/bottom-right and top-right/bottom-left) spells either
"MAS" or "SAM".
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return how many X-MAS patterns appear in the grid."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            if grid[r][c] != "A":
                continue
            d1 = grid[r - 1][c - 1] + grid[r + 1][c + 1]
            d2 = grid[r - 1][c + 1] + grid[r + 1][c - 1]
            if d1 in ("MS", "SM") and d2 in ("MS", "SM"):
                count += 1
    return count


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d4_input.txt").read_text()))
