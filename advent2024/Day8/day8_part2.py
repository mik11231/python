#!/usr/bin/env python3
"""Advent of Code 2024 Day 8 Part 2 - Resonant Collinearity.

Antinodes now occur at every grid position collinear with any pair of
same-frequency antennas. Walk both directions from each pair using the
GCD-reduced step vector to enumerate all collinear grid points.
"""
from pathlib import Path
from collections import defaultdict
from itertools import combinations
from math import gcd


def solve(s: str) -> int:
    """Return number of unique antinode locations (collinear model)."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    antennas = defaultdict(list)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '.':
                antennas[grid[r][c]].append((r, c))

    antinodes = set()
    for positions in antennas.values():
        for (r1, c1), (r2, c2) in combinations(positions, 2):
            dr, dc = r2 - r1, c2 - c1
            g = gcd(abs(dr), abs(dc))
            dr, dc = dr // g, dc // g
            cr, cc = r1, c1
            while 0 <= cr < rows and 0 <= cc < cols:
                antinodes.add((cr, cc))
                cr += dr
                cc += dc
            cr, cc = r1 - dr, c1 - dc
            while 0 <= cr < rows and 0 <= cc < cols:
                antinodes.add((cr, cc))
                cr -= dr
                cc -= dc
    return len(antinodes)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d8_input.txt").read_text()))
