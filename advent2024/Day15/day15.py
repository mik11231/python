#!/usr/bin/env python3
"""Advent of Code 2024 Day 15 Part 1 - Warehouse Woes.

Simulate a robot pushing single-cell boxes (O) around a grid.
The robot moves in the given directions; if a box is in the way,
it pushes the whole chain of boxes forward (if there is room).
Sum of all boxes' GPS coordinates (100*row + col) after all moves.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return sum of GPS coordinates of all boxes after simulation."""
    grid_part, moves_part = s.split("\n\n")
    grid = [list(row) for row in grid_part.splitlines()]
    moves = moves_part.replace("\n", "")

    rows, cols = len(grid), len(grid[0])
    dirs = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

    rr = rc = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                rr, rc = r, c
                grid[r][c] = '.'
                break

    for m in moves:
        dr, dc = dirs[m]
        nr, nc = rr + dr, rc + dc
        if grid[nr][nc] == '#':
            continue
        if grid[nr][nc] == '.':
            rr, rc = nr, nc
            continue
        # box chain
        er, ec = nr, nc
        while grid[er][ec] == 'O':
            er, ec = er + dr, ec + dc
        if grid[er][ec] == '#':
            continue
        grid[er][ec] = 'O'
        grid[nr][nc] = '.'
        rr, rc = nr, nc

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'O':
                total += 100 * r + c
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d15_input.txt").read_text()))
