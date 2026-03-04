#!/usr/bin/env python3
"""Advent of Code 2024 Day 4 Part 1 — Ceres Search.

Word search: count all occurrences of "XMAS" in all 8 directions (horizontal,
vertical, diagonal, and their reverses) in a grid of letters.
"""
from pathlib import Path

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
WORD = "XMAS"


def solve(s: str) -> int:
    """Return how many times XMAS appears in all 8 directions."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    count = 0
    for r in range(rows):
        for c in range(cols):
            for dr, dc in DIRS:
                if all(
                    0 <= r + dr * k < rows
                    and 0 <= c + dc * k < cols
                    and grid[r + dr * k][c + dc * k] == WORD[k]
                    for k in range(4)
                ):
                    count += 1
    return count


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d4_input.txt").read_text()))
