#!/usr/bin/env python3
"""Advent of Code 2024 Day 20 Part 1 - Race Condition.

BFS from S to E on a grid to get distances. A cheat passes through exactly one
wall cell (2 steps). For every pair of track cells with Manhattan distance == 2,
compute time saved = |dist[a] - dist[b]| - 2. Count cheats saving >= 100.
"""
from pathlib import Path
from collections import deque


def solve(s: str, threshold: int = 100) -> int:
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'E':
                end = (r, c)

    dist = {start: 0}
    q = deque([start])
    while q:
        r, c = q.popleft()
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in dist and grid[nr][nc] != '#':
                dist[(nr, nc)] = dist[(r, c)] + 1
                q.append((nr, nc))

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
