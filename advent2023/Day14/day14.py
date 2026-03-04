#!/usr/bin/env python3
"""Advent of Code 2023 Day 14 Part 1 - Parabolic Reflector Dish.

Tilt the platform north so all rounded rocks (O) slide up until blocked by
cube rocks (#) or the top edge.  The load of each O is (total_rows - row).
"""
from pathlib import Path


def tilt_north(grid: list[list[str]]) -> list[list[str]]:
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
    return grid


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    grid = [list(line) for line in s.strip().splitlines()]
    grid = tilt_north(grid)
    rows = len(grid)
    return sum(rows - r for r in range(rows) for c in range(len(grid[0])) if grid[r][c] == "O")


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d14_input.txt").read_text()))
