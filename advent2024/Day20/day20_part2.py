#!/usr/bin/env python3
"""Advent of Code 2024 Day 20 Part 2 - Race Condition (20-step cheats).

Same grid BFS for distances. A cheat can last up to 20 steps through walls.
For every pair (a, b) of track cells where Manhattan distance <= 20,
saved = dist[b] - dist[a] - manhattan(a,b). Count pairs where saved >= 100.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.geometry import manhattan2
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

    track = list(dist.items())
    count = 0
    for i, ((r1, c1), d1) in enumerate(track):
        for j in range(i + 1, len(track)):
            (r2, c2), d2 = track[j]
            md = manhattan2((r1, c1), (r2, c2))
            if md <= 20:
                saved = abs(d2 - d1) - md
                if saved >= threshold:
                    count += 1
    return count


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d20_input.txt").read_text()))
