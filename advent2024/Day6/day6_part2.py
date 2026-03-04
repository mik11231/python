#!/usr/bin/env python3
"""Advent of Code 2024 Day 6 Part 2 — Guard Gallivant (loop detection).

Count how many empty positions could have a new obstacle placed to trap the
guard in a loop. Only positions on the original patrol path are candidates.
Detect loops by tracking (row, col, direction) states.
"""
from pathlib import Path

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
DR = [-1, 0, 1, 0]
DC = [0, 1, 0, -1]


def patrol_path(grid, rows, cols, sr, sc, sd):
    """Return set of positions visited, or None if a loop is detected."""
    r, c, d = sr, sc, sd
    visited = set()
    states = set()
    while 0 <= r < rows and 0 <= c < cols:
        state = (r, c, d)
        if state in states:
            return None
        states.add(state)
        visited.add((r, c))
        nr, nc = r + DR[d], c + DC[d]
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "#":
            d = (d + 1) % 4
        else:
            r, c = nr, nc
    return visited


def solve(s: str) -> int:
    """Return the number of positions where a new obstacle creates a loop."""
    grid = [list(row) for row in s.strip().splitlines()]
    rows, cols = len(grid), len(grid[0])

    sr = sc = sd = 0
    for ri in range(rows):
        for ci in range(cols):
            if grid[ri][ci] == "^":
                sr, sc, sd = ri, ci, UP

    candidates = patrol_path(grid, rows, cols, sr, sc, sd)
    candidates.discard((sr, sc))

    count = 0
    for r, c in candidates:
        grid[r][c] = "#"
        if patrol_path(grid, rows, cols, sr, sc, sd) is None:
            count += 1
        grid[r][c] = "."
    return count


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d6_input.txt").read_text()))
