#!/usr/bin/env python3
"""Advent of Code 2024 Day 18 Part 2 - RAM Run (first blocking byte).

Binary search for the first byte index where the path from (0,0) to
(70,70) becomes blocked. Return that byte's coordinates as "x,y".
"""
from pathlib import Path
from collections import deque


def has_path(corrupted, size):
    """Return True if a path exists from (0,0) to (size-1,size-1)."""
    goal = (size - 1, size - 1)
    if (0, 0) in corrupted or goal in corrupted:
        return False
    visited = {(0, 0)}
    q = deque([(0, 0)])
    while q:
        x, y = q.popleft()
        if (x, y) == goal:
            return True
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < size and 0 <= ny < size and (nx, ny) not in visited and (nx, ny) not in corrupted:
                visited.add((nx, ny))
                q.append((nx, ny))
    return False


def solve(s: str, size: int = 71) -> str:
    """Return 'x,y' of the first byte that blocks the path."""
    coords = []
    for line in s.strip().splitlines():
        x, y = map(int, line.split(","))
        coords.append((x, y))

    lo, hi = 0, len(coords) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if has_path(set(coords[:mid + 1]), size):
            lo = mid + 1
        else:
            hi = mid
    x, y = coords[lo]
    return f"{x},{y}"


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d18_input.txt").read_text()))
