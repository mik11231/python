#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 25: Sea Cucumber (Part 1)

East-facing ('>') and south-facing ('v') sea cucumbers move on a
toroidal grid.  Each step has two phases:

1. All east-movers simultaneously try to move one space right (wrapping).
2. All south-movers simultaneously try to move one space down (wrapping).

A cucumber moves only if its destination cell is empty (after any same-
phase moves are accounted for simultaneously).

Algorithm
---------
Use a set for each herd.  On each half-step, compute which cucumbers can
move (destination is free of *all* cucumbers), then apply all moves at
once.  Stop when no cucumber moves.
"""

from pathlib import Path


def parse_grid(
    text: str,
) -> tuple[int, int, set[tuple[int, int]], set[tuple[int, int]]]:
    """Return (rows, cols, east_set, south_set)."""
    lines = text.strip().splitlines()
    rows, cols = len(lines), len(lines[0])
    east: set[tuple[int, int]] = set()
    south: set[tuple[int, int]] = set()
    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == ">":
                east.add((r, c))
            elif ch == "v":
                south.add((r, c))
    return rows, cols, east, south


def simulate(
    rows: int,
    cols: int,
    east: set[tuple[int, int]],
    south: set[tuple[int, int]],
) -> int:
    """Return the first step on which no sea cucumber moves."""
    step = 0
    while True:
        step += 1
        moved = False

        new_east: set[tuple[int, int]] = set()
        for r, c in east:
            nc = (c + 1) % cols
            if (r, nc) not in east and (r, nc) not in south:
                new_east.add((r, nc))
                moved = True
            else:
                new_east.add((r, c))
        east = new_east

        new_south: set[tuple[int, int]] = set()
        for r, c in south:
            nr = (r + 1) % rows
            if (nr, c) not in east and (nr, c) not in south:
                new_south.add((nr, c))
                moved = True
            else:
                new_south.add((r, c))
        south = new_south

        if not moved:
            return step


def solve(input_path: str = "advent2021/Day25/d25_input.txt") -> int:
    """Return the first step where no cucumber moves."""
    text = Path(input_path).read_text()
    rows, cols, east, south = parse_grid(text)
    return simulate(rows, cols, east, south)


if __name__ == "__main__":
    print(f"First step with no movement: {solve()}")
