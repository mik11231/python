#!/usr/bin/env python3
"""Advent of Code 2023 Day 18 Part 1 - Lavaduct Lagoon.

Parse dig instructions (direction + distance), trace the trench vertices,
then compute the enclosed area using the Shoelace formula + Pick's theorem.
"""
from pathlib import Path

DIRS = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    r, c = 0, 0
    vertices = [(r, c)]
    perimeter = 0

    for line in s.strip().splitlines():
        parts = line.split()
        d, n = parts[0], int(parts[1])
        dr, dc = DIRS[d]
        r += dr * n
        c += dc * n
        vertices.append((r, c))
        perimeter += n

    # Shoelace formula for double area
    area2 = 0
    for i in range(len(vertices) - 1):
        r1, c1 = vertices[i]
        r2, c2 = vertices[i + 1]
        area2 += r1 * c2 - r2 * c1

    interior = abs(area2) // 2 - perimeter // 2 + 1
    return interior + perimeter


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d18_input.txt").read_text()))
