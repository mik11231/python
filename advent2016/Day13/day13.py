#!/usr/bin/env python3
"""Advent of Code 2016 Day 13 Part 1: A Maze of Twisty Little Cubicles."""

from collections import deque
from pathlib import Path


def wall(x: int, y: int, fav: int) -> bool:
    """Return True when (x,y) is a wall."""
    v = x * x + 3 * x + 2 * x * y + y + y * y + fav
    return bin(v).count("1") % 2 == 1


def solve(s: str) -> int:
    """Return shortest steps from (1,1) to (31,39)."""
    fav = int(s.strip())
    target = (31, 39)
    q = deque([(1, 1, 0)])
    seen = {(1, 1)}
    while q:
        x, y, d = q.popleft()
        if (x, y) == target:
            return d
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nx < 0 or ny < 0:
                continue
            if wall(nx, ny, fav):
                continue
            if (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append((nx, ny, d + 1))
    raise ValueError("Target unreachable")


if __name__ == "__main__":
    text = Path(__file__).with_name("d13_input.txt").read_text(encoding="utf-8")
    print(solve(text))
