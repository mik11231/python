#!/usr/bin/env python3
"""Advent of Code 2023 Day 14 Part 2 - Parabolic Reflector Dish.

Perform 1 billion spin cycles (N, W, S, E tilts).  Detect a cycle in the
grid states to skip ahead instead of simulating all iterations.
"""
from pathlib import Path


def tilt_north(grid: list[list[str]]) -> None:
    rows, cols = len(grid), len(grid[0])
    for c in range(cols):
        empty = 0
        for r in range(rows):
            if grid[r][c] == "O":
                grid[r][c] = "."
                grid[empty][c] = "O"
                empty += 1
            elif grid[r][c] == "#":
                empty = r + 1


def tilt_south(grid: list[list[str]]) -> None:
    rows, cols = len(grid), len(grid[0])
    for c in range(cols):
        empty = rows - 1
        for r in range(rows - 1, -1, -1):
            if grid[r][c] == "O":
                grid[r][c] = "."
                grid[empty][c] = "O"
                empty -= 1
            elif grid[r][c] == "#":
                empty = r - 1


def tilt_west(grid: list[list[str]]) -> None:
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        empty = 0
        for c in range(cols):
            if grid[r][c] == "O":
                grid[r][c] = "."
                grid[r][empty] = "O"
                empty += 1
            elif grid[r][c] == "#":
                empty = c + 1


def tilt_east(grid: list[list[str]]) -> None:
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        empty = cols - 1
        for c in range(cols - 1, -1, -1):
            if grid[r][c] == "O":
                grid[r][c] = "."
                grid[r][empty] = "O"
                empty -= 1
            elif grid[r][c] == "#":
                empty = c - 1


def spin_cycle(grid: list[list[str]]) -> None:
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


def grid_key(grid: list[list[str]]) -> tuple:
    return tuple(tuple(row) for row in grid)


def load(grid: list[list[str]]) -> int:
    rows = len(grid)
    return sum(rows - r for r in range(rows) for c in range(len(grid[0])) if grid[r][c] == "O")


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    grid = [list(line) for line in s.strip().splitlines()]
    seen: dict[tuple, int] = {}
    target = 1_000_000_000

    for i in range(target):
        key = grid_key(grid)
        if key in seen:
            cycle_len = i - seen[key]
            remaining = (target - i) % cycle_len
            for _ in range(remaining):
                spin_cycle(grid)
            return load(grid)
        seen[key] = i
        spin_cycle(grid)

    return load(grid)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d14_input.txt").read_text()))
