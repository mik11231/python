#!/usr/bin/env python3
"""Advent of Code 2015 Day 18 Part 2 — Corners stuck on.

Same 100 steps but four corners are always on.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines

from day18 import STEPS, parse, count_neighbors


def step(grid: list[list[bool]]) -> list[list[bool]]:
    """One step with corners stuck on."""
    R, C = len(grid), len(grid[0])
    next_grid = [[False] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            n = count_neighbors(grid, r, c)
            if grid[r][c]:
                next_grid[r][c] = n in (2, 3)
            else:
                next_grid[r][c] = n == 3
    next_grid[0][0] = next_grid[0][C - 1] = next_grid[R - 1][0] = next_grid[R - 1][C - 1] = True
    return next_grid


def solve(s: str) -> int:
    """Run 100 steps with corners stuck on; return count on."""
    grid = parse(s)
    R, C = len(grid), len(grid[0])
    grid[0][0] = grid[0][C - 1] = grid[R - 1][0] = grid[R - 1][C - 1] = True
    for _ in range(STEPS):
        grid = step(grid)
    return sum(1 for row in grid for c in row if c)


if __name__ == "__main__":
    text = Path(__file__).with_name("d18_input.txt").read_text(encoding="utf-8")
    print(solve(text))
