#!/usr/bin/env python3
"""Advent of Code 2016 Day 22 Part 2: move goal data to (0,0)."""

from collections import deque
from pathlib import Path
import re


NODE_RE = re.compile(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T")


def parse(s: str):
    """Parse nodes and grid metadata."""
    nodes = []
    max_x = max_y = 0
    for ln in s.splitlines():
        m = NODE_RE.search(ln)
        if not m:
            continue
        x, y, size, used, avail = map(int, m.groups())
        nodes.append((x, y, size, used, avail))
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return nodes, max_x, max_y


def solve(s: str) -> int:
    """Compute minimum moves by moving empty node near goal and shifting left."""
    nodes, max_x, max_y = parse(s)
    used = {(x, y): u for x, y, _, u, _ in nodes}
    size = {(x, y): sz for x, y, sz, _, _ in nodes}
    empty = next((x, y) for x, y, _, u, _ in nodes if u == 0)

    # Nodes too large to receive data from empty are walls.
    empty_cap = size[empty]
    walls = {(x, y) for x, y in used if used[(x, y)] > empty_cap}

    goal = (max_x, 0)
    target = (goal[0] - 1, 0)

    q = deque([(empty[0], empty[1], 0)])
    seen = {empty}
    dist = None
    while q:
        x, y, d = q.popleft()
        if (x, y) == target:
            dist = d
            break
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if not (0 <= nx <= max_x and 0 <= ny <= max_y):
                continue
            if (nx, ny) in walls:
                continue
            if (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append((nx, ny, d + 1))

    if dist is None:
        raise ValueError("Could not reach left-of-goal position")

    # One move to swap with goal, then 5 moves per left shift across remaining columns.
    return dist + 1 + 5 * (goal[0] - 1)


if __name__ == "__main__":
    text = Path(__file__).with_name("d22_input.txt").read_text(encoding="utf-8")
    print(solve(text))
