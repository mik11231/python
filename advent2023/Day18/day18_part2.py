#!/usr/bin/env python3
"""Advent of Code 2023 Day 18 Part 2 - Lavaduct Lagoon.

The hex color codes encode the real instructions: first 5 hex digits are the
distance, last hex digit is direction (0=R,1=D,2=L,3=U).  Same Shoelace+Pick's.
"""
from pathlib import Path

DIR_MAP = {0: (0, 1), 1: (1, 0), 2: (0, -1), 3: (-1, 0)}


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    r, c = 0, 0
    vertices = [(r, c)]
    perimeter = 0

    for line in s.strip().splitlines():
        hex_code = line.split()[-1]
        n = int(hex_code[2:7], 16)
        d = int(hex_code[7])
        dr, dc = DIR_MAP[d]
        r += dr * n
        c += dc * n
        vertices.append((r, c))
        perimeter += n

    area2 = 0
    for i in range(len(vertices) - 1):
        r1, c1 = vertices[i]
        r2, c2 = vertices[i + 1]
        area2 += r1 * c2 - r2 * c1

    interior = abs(area2) // 2 - perimeter // 2 + 1
    return interior + perimeter


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d18_input.txt").read_text()))
