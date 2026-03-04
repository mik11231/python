#!/usr/bin/env python3
"""Advent of Code 2024 Day 20 Part 1 - Race Condition.

BFS from S to E on a grid to get distances. A cheat passes through exactly one
wall cell (2 steps). For every pair of track cells with Manhattan distance == 2,
compute time saved = |dist[a] - dist[b]| - 2. Count cheats saving >= 100.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.grid import neighbors4
from aoclib.search import bfs_distances


def solve(s: str, threshold: int = 100) -> int:
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)

    def _neighbors(cell: tuple[int, int]):
        r, c = cell
        for nr, nc in neighbors4(r, c, rows, cols):
            if grid[nr][nc] != '#':
                yield (nr, nc)

    dist = bfs_distances(start, _neighbors)

    count = 0
    for (r, c), d in dist.items():
        for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) in dist:
                saved = dist[(nr, nc)] - d - 2
                if saved >= threshold:
                    count += 1
    return count


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d20_input.txt").read_text()))
