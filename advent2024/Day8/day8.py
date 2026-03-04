#!/usr/bin/env python3
"""Advent of Code 2024 Day 8 Part 1 - Resonant Collinearity.

Find antinodes of same-frequency antenna pairs on a grid. For each pair,
two antinodes exist where one antenna is twice as far as the other.
Count unique antinode positions within the grid bounds.
"""
from pathlib import Path
from collections import defaultdict
from itertools import combinations


def solve(s: str) -> int:
    """Return number of unique antinode locations within the map."""
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
            for ar, ac in [(2 * r1 - r2, 2 * c1 - c2),
                           (2 * r2 - r1, 2 * c2 - c1)]:
                if 0 <= ar < rows and 0 <= ac < cols:
                    antinodes.add((ar, ac))
    return len(antinodes)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d8_input.txt").read_text()))
