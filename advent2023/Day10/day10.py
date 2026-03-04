#!/usr/bin/env python3
"""Advent of Code 2023 Day 10 Part 1 — Pipe Maze.

Find the main loop starting at 'S' by BFS along connected pipes.
The answer is half the loop length (farthest point from start).
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


def find_loop(grid: list[str]) -> list[tuple[int, int]]:
    """Return the ordered list of positions forming the main loop."""
    rows = len(grid)
    sr = sc = 0
    for r in range(rows):
        for c in range(len(grid[r])):
            if grid[r][c] == "S":
                sr, sc = r, c

    q: deque[tuple[int, int]] = deque([(sr, sc)])
    visited: dict[tuple[int, int], int] = {(sr, sc): 0}

    while q:
        r, c = q.popleft()
        ch = _char(grid, r, c)
        for dr, dc in CONNECTIONS.get(ch, set()):
            nr, nc = r + dr, c + dc
            if (nr, nc) not in visited:
                nch = _char(grid, nr, nc)
                if (-dr, -dc) in CONNECTIONS.get(nch, set()):
                    visited[(nr, nc)] = visited[(r, c)] + 1
                    q.append((nr, nc))

    return list(visited.keys())


def solve(s: str) -> int:
    """Return the distance of the farthest point in the loop from S."""
    grid = s.strip().splitlines()
    loop = find_loop(grid)
    return len(loop) // 2


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d10_input.txt").read_text()))
