#!/usr/bin/env python3
"""Advent of Code 2015 Day 18 — Like a GIF For Your Yard.

100x100 grid, Conway-like: on if 2 or 3 neighbors on; off turns on if 3 neighbors on.
Part 1: 100 steps, count on.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


STEPS = 100


def parse(s: str) -> list[list[bool]]:
    """Return grid: True = on (#), False = off (.)."""
    grid = []
    for line in lines(s):
        line = line.strip()
        if not line:
            continue
        grid.append([c == "#" for c in line])
    return grid


def count_neighbors(grid: list[list[bool]], r: int, c: int) -> int:
    """Count on neighbors (8 directions)."""
    R, C = len(grid), len(grid[0])
    n = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc]:
                n += 1
    return n


def step(grid: list[list[bool]]) -> list[list[bool]]:
    """One step: on with 2 or 3 neighbors stays on; off with 3 turns on."""
    R, C = len(grid), len(grid[0])
    next_grid = [[False] * C for _ in range(R)]
    for r in range(R):
        for c in range(C):
            n = count_neighbors(grid, r, c)
            if grid[r][c]:
                next_grid[r][c] = n in (2, 3)
            else:
                next_grid[r][c] = n == 3
    return next_grid


def solve(s: str) -> int:
    """Run 100 steps and return count of lights on."""
    grid = parse(s)
    for _ in range(STEPS):
        grid = step(grid)
    return sum(1 for row in grid for c in row if c)


if __name__ == "__main__":
    text = Path(__file__).with_name("d18_input.txt").read_text(encoding="utf-8")
    print(solve(text))
