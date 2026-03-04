#!/usr/bin/env python3
"""Advent of Code 2017 Day 3 Part 2."""

from collections import defaultdict
from pathlib import Path


NEI = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def solve(s: str) -> int:
    target = int(s.strip())
    g = defaultdict(int)
    x = y = 0
    g[(0, 0)] = 1
    step = 1
    while True:
        for _ in range(step):
            x += 1
            v = sum(g[(x + dx, y + dy)] for dx, dy in NEI)
            if v > target:
                return v
            g[(x, y)] = v
        for _ in range(step):
            y += 1
            v = sum(g[(x + dx, y + dy)] for dx, dy in NEI)
            if v > target:
                return v
            g[(x, y)] = v
        step += 1
        for _ in range(step):
            x -= 1
            v = sum(g[(x + dx, y + dy)] for dx, dy in NEI)
            if v > target:
                return v
            g[(x, y)] = v
        for _ in range(step):
            y -= 1
            v = sum(g[(x + dx, y + dy)] for dx, dy in NEI)
            if v > target:
                return v
            g[(x, y)] = v
        step += 1


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d3_input.txt").read_text(encoding="utf-8")))
