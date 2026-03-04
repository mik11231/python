#!/usr/bin/env python3
"""Advent of Code 2024 Day 6 Part 1 — Guard Gallivant.

Simulate a guard walking on a grid. The guard starts facing up (^) and turns
right 90 degrees when hitting an obstacle (#). Count distinct positions visited
before the guard leaves the map.
"""
from pathlib import Path

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
DR = [-1, 0, 1, 0]
DC = [0, 1, 0, -1]


def solve(s: str) -> int:
    """Return the number of distinct positions the guard visits."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    r = c = d = 0
    for ri, row in enumerate(grid):
        for ci, ch in enumerate(row):
            if ch == "^":
                r, c, d = ri, ci, UP

    visited = set()
    while 0 <= r < rows and 0 <= c < cols:
        visited.add((r, c))
        nr, nc = r + DR[d], c + DC[d]
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "#":
            d = (d + 1) % 4
        else:
            r, c = nr, nc
    return len(visited)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d6_input.txt").read_text()))
