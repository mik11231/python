#!/usr/bin/env python3
"""Advent of Code 2016 Day 17 Part 2: longest vault path length."""

from collections import deque
import hashlib
from pathlib import Path


OPEN = set("bcdef")


def solve(s: str) -> int:
    """Return length of longest path that reaches the goal."""
    code = s.strip()
    q = deque([(0, 0, "")])
    best = 0
    while q:
        x, y, p = q.popleft()
        if (x, y) == (3, 3):
            best = max(best, len(p))
            continue
        h = hashlib.md5((code + p).encode("utf-8")).hexdigest()[:4]
        for ch, (dx, dy), step in zip(h, ((0, -1), (0, 1), (-1, 0), (1, 0)), "UDLR"):
            nx, ny = x + dx, y + dy
            if ch in OPEN and 0 <= nx < 4 and 0 <= ny < 4:
                q.append((nx, ny, p + step))
    return best


if __name__ == "__main__":
    text = Path(__file__).with_name("d17_input.txt").read_text(encoding="utf-8")
    print(solve(text))
