#!/usr/bin/env python3
"""Advent of Code 2023 Day 21 Part 1 - Step Counter.

BFS on garden grid to find how many garden plots are reachable in exactly
64 steps. A position is reachable at step N if its shortest BFS distance
shares the same parity as N.
"""
from pathlib import Path
from collections import deque


def solve(s: str, steps: int = 64) -> int:
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    sr = sc = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                sr, sc = r, c

    dist = {(sr, sc): 0}
    queue = deque([(sr, sc, 0)])
    while queue:
        r, c, d = queue.popleft()
        if d >= steps:
            continue
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = d + 1
                queue.append((nr, nc, d + 1))

    return sum(1 for v in dist.values() if v % 2 == steps % 2)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d21_input.txt").read_text()))
