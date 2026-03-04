#!/usr/bin/env python3
"""Advent of Code 2024 Day 18 Part 1 - RAM Run.

BFS shortest path on a 71x71 grid (coords 0-70) from (0,0) to (70,70)
after the first 1024 bytes have fallen and corrupted those cells.
"""
from pathlib import Path
from collections import deque


def bfs(corrupted, size):
    """Return shortest path length from (0,0) to (size-1,size-1), or -1."""
    goal = (size - 1, size - 1)
    if (0, 0) in corrupted or goal in corrupted:
        return -1
    visited = {(0, 0)}
    q = deque([(0, 0, 0)])
    while q:
        x, y, d = q.popleft()
        if (x, y) == goal:
            return d
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in visited and (nx, ny) not in corrupted:
                visited.add((nx, ny))
                q.append((nx, ny, d + 1))
    return -1


def solve(s: str, size: int = 71, n_bytes: int = 1024) -> int:
    """Return minimum steps to reach exit after n_bytes have fallen."""
    coords = []
    for line in s.strip().splitlines():
        x, y = map(int, line.split(","))
        coords.append((x, y))
    corrupted = set(coords[:n_bytes])
    return bfs(corrupted, size)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d18_input.txt").read_text()))
