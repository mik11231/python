#!/usr/bin/env python3
"""Advent of Code 2023 Day 21 Part 2 - Step Counter.

On an infinite tiling grid, count reachable plots in 26501365 steps.
The grid is 131x131 with start at center; 26501365 = 202300*131 + 65.
BFS for 65, 196, 327 steps on the infinite grid, then use quadratic
extrapolation to find the value at n=202300.
"""
from pathlib import Path
from collections import deque


def count_reachable(grid, rows, cols, sr, sc, steps):
    dist = {(sr, sc): 0}
    queue = deque([(sr, sc, 0)])
    while queue:
        r, c, d = queue.popleft()
        if d >= steps:
            continue
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if grid[nr % rows][nc % cols] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = d + 1
                queue.append((nr, nc, d + 1))
    return sum(1 for v in dist.values() if v % 2 == steps % 2)


def solve(s: str) -> int:
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    sr = sc = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                sr, sc = r, c

    half = rows // 2
    target = 26501365
    n = target // rows

    y0 = count_reachable(grid, rows, cols, sr, sc, half)
    y1 = count_reachable(grid, rows, cols, sr, sc, half + rows)
    y2 = count_reachable(grid, rows, cols, sr, sc, half + 2 * rows)

    c = y0
    a = (y2 - 2 * y1 + y0) // 2
    b = y1 - y0 - a

    return a * n * n + b * n + c


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d21_input.txt").read_text()))
