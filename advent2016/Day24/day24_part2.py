#!/usr/bin/env python3
"""Advent of Code 2016 Day 24 Part 2: return to start."""

from collections import deque
from itertools import permutations
from pathlib import Path


def bfs(grid: list[str], sr: int, sc: int) -> dict[tuple[int, int], int]:
    """BFS distances from one grid location."""
    h, w = len(grid), len(grid[0])
    q = deque([(sr, sc, 0)])
    seen = {(sr, sc)}
    out = {(sr, sc): 0}
    while q:
        r, c, d = q.popleft()
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if not (0 <= nr < h and 0 <= nc < w):
                continue
            if grid[nr][nc] == "#" or (nr, nc) in seen:
                continue
            seen.add((nr, nc))
            out[(nr, nc)] = d + 1
            q.append((nr, nc, d + 1))
    return out


def solve(s: str) -> int:
    """Return shortest path visiting all points and returning to 0."""
    grid = [ln for ln in s.splitlines() if ln]
    pts: dict[int, tuple[int, int]] = {}
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch.isdigit():
                pts[int(ch)] = (r, c)

    keys = sorted(pts)
    dist: dict[tuple[int, int], int] = {}
    for a in keys:
        dmap = bfs(grid, *pts[a])
        for b in keys:
            if a != b:
                dist[(a, b)] = dmap[pts[b]]

    others = [k for k in keys if k != 0]
    best = 10**9
    for perm in permutations(others):
        cur = 0
        total = 0
        for nxt in perm:
            total += dist[(cur, nxt)]
            cur = nxt
        total += dist[(cur, 0)]
        best = min(best, total)
    return best


if __name__ == "__main__":
    text = Path(__file__).with_name("d24_input.txt").read_text(encoding="utf-8")
    print(solve(text))
