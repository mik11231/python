#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 17: Conway Cubes (Part 1)

A 3-D (or N-D) Conway Game of Life on an infinite grid.  The initial state is
a 2-D slice at z=0 (and w=0, etc. for higher dimensions).

Rules each cycle (applied simultaneously):
  - An active cell with exactly 2 or 3 active neighbors stays active.
  - An inactive cell with exactly 3 active neighbors becomes active.

Algorithm
---------
Sparse-set simulation: store only the coordinates of active cells.  Each cycle,
collect every neighbor of every active cell (the "frontier"), count how many
active neighbors each frontier cell has, then apply the rules.

The `simulate` function works for arbitrary dimensions by representing each
coordinate as a tuple of length *dimensions*.
"""

from collections import Counter
from itertools import product
from pathlib import Path


def _neighbors(coord: tuple[int, ...]) -> list[tuple[int, ...]]:
    """Return all adjacent coordinates (excluding *coord* itself)."""
    offsets = product((-1, 0, 1), repeat=len(coord))
    zero = (0,) * len(coord)
    return [tuple(c + d for c, d in zip(coord, delta)) for delta in offsets if delta != zero]


def simulate(
    initial_active: set[tuple[int, ...]],
    dimensions: int = 3,
    cycles: int = 6,
) -> set[tuple[int, ...]]:
    """Run the N-D Conway simulation and return the final set of active cells."""
    active = set(initial_active)
    for _ in range(cycles):
        neighbor_counts: Counter[tuple[int, ...]] = Counter()
        for coord in active:
            for nb in _neighbors(coord):
                neighbor_counts[nb] += 1

        new_active: set[tuple[int, ...]] = set()
        for coord, count in neighbor_counts.items():
            if coord in active and count in (2, 3):
                new_active.add(coord)
            elif coord not in active and count == 3:
                new_active.add(coord)
        active = new_active
    return active


def parse_initial_state(text: str, dimensions: int = 3) -> set[tuple[int, ...]]:
    """Parse the 2-D text grid into a set of N-D coordinates (extra dims = 0)."""
    active: set[tuple[int, ...]] = set()
    for y, line in enumerate(text.strip().splitlines()):
        for x, ch in enumerate(line):
            if ch == "#":
                coord = (x, y) + (0,) * (dimensions - 2)
                active.add(coord)
    return active


def solve(input_path: str = "advent2020/Day17/d17_input.txt") -> int:
    """Return the number of active cubes after 6 cycles in 3-D."""
    text = Path(input_path).read_text()
    initial = parse_initial_state(text, dimensions=3)
    final = simulate(initial, dimensions=3, cycles=6)
    return len(final)


if __name__ == "__main__":
    result = solve()
    print(f"Active cubes after 6 cycles (3D): {result}")
