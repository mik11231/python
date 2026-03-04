#!/usr/bin/env python3
"""Advent of Code 2023 Day 22 Part 2 - Sand Slabs.

For each brick, calculate how many other bricks would fall if it were removed,
using BFS to propagate chain reactions. Sum all counts.
"""
from pathlib import Path
from collections import deque


def settle(bricks):
    bricks.sort(key=lambda b: min(b[2], b[5]))
    n = len(bricks)
    supports = [set() for _ in range(n)]
    supported_by = [set() for _ in range(n)]
    height_map = {}

    for i, (x1, y1, z1, x2, y2, z2) in enumerate(bricks):
        cells = [
            (x, y)
            for x in range(min(x1, x2), max(x1, x2) + 1)
            for y in range(min(y1, y2), max(y1, y2) + 1)
        ]
        max_z = 0
        for xy in cells:
            if xy in height_map:
                max_z = max(max_z, height_map[xy][0])

        for xy in cells:
            if xy in height_map and height_map[xy][0] == max_z and max_z > 0:
                supporter = height_map[xy][1]
                supports[i].add(supporter)
                supported_by[supporter].add(i)

        dz = min(z1, z2) - max_z - 1
        top_z = max(z1, z2) - dz
        for xy in cells:
            height_map[xy] = (top_z, i)

    return supports, supported_by


def solve(s: str) -> int:
    bricks = []
    for line in s.strip().splitlines():
        a, b = line.split("~")
        bricks.append((*map(int, a.split(",")), *map(int, b.split(","))))

    supports, supported_by = settle(bricks)

    total = 0
    for i in range(len(bricks)):
        fallen = {i}
        queue = deque(j for j in supported_by[i] if supports[j] <= fallen)
        fallen.update(queue)
        while queue:
            brick = queue.popleft()
            for j in supported_by[brick]:
                if j not in fallen and supports[j] <= fallen:
                    fallen.add(j)
                    queue.append(j)
        total += len(fallen) - 1

    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d22_input.txt").read_text()))
