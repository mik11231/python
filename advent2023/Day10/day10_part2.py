#!/usr/bin/env python3
"""Advent of Code 2023 Day 10 Part 2 — Pipe Maze.

Count tiles enclosed by the main loop.  Walk the loop to get ordered vertices,
compute the interior area via the shoelace formula, then apply Pick's theorem:
    A = i + b/2 - 1  =>  i = A - b/2 + 1
where b = boundary points (loop length) and i = interior points (answer).
"""
from pathlib import Path
from collections import deque

CONNECTIONS = {
    "|": {(-1, 0), (1, 0)},
    "-": {(0, -1), (0, 1)},
    "L": {(-1, 0), (0, 1)},
    "J": {(-1, 0), (0, -1)},
    "7": {(1, 0), (0, -1)},
    "F": {(1, 0), (0, 1)},
    ".": set(),
    "S": {(-1, 0), (1, 0), (0, -1), (0, 1)},
}


def _char(grid: list[str], r: int, c: int) -> str:
    """
    Run `_char` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid, r, c.
    - Returns the computed result for this stage of the pipeline.
    """
    if 0 <= r < len(grid) and 0 <= c < len(grid[r]):
        return grid[r][c]
    return "."


def get_loop_ordered(grid: list[str]) -> list[tuple[int, int]]:
    """Return positions of the main loop in traversal order."""
    rows = len(grid)
    sr = sc = 0
    for r in range(rows):
        for c in range(len(grid[r])):
            if grid[r][c] == "S":
                sr, sc = r, c

    first = None
    for dr, dc in CONNECTIONS["S"]:
        nr, nc = sr + dr, sc + dc
        nch = _char(grid, nr, nc)
        if (-dr, -dc) in CONNECTIONS.get(nch, set()):
            first = (nr, nc)
            break

    path = [(sr, sc), first]
    while path[-1] != (sr, sc) or len(path) == 2:
        r, c = path[-1]
        ch = _char(grid, r, c)
        for dr, dc in CONNECTIONS.get(ch, set()):
            nr, nc = r + dr, c + dc
            if (nr, nc) != path[-2]:
                nch = _char(grid, nr, nc)
                if (-dr, -dc) in CONNECTIONS.get(nch, set()):
                    if (nr, nc) == (sr, sc):
                        return path
                    path.append((nr, nc))
                    break
    return path


def solve(s: str) -> int:
    """Return the number of tiles enclosed by the loop."""
    grid = s.strip().splitlines()
    loop = get_loop_ordered(grid)
    b = len(loop)

    area2 = 0
    for i in range(b):
        r1, c1 = loop[i]
        r2, c2 = loop[(i + 1) % b]
        area2 += r1 * c2 - r2 * c1

    area = abs(area2) // 2
    interior = area - b // 2 + 1
    return interior


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d10_input.txt").read_text()))
