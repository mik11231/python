#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 24: Lobby Layout (Part 2)

After the initial tile flips, run a hex-grid Game of Life for 100 days.
Each day, simultaneously:
  - A black tile with 0 or >2 black neighbours flips to white.
  - A white tile with exactly 2 black neighbours flips to black.

Algorithm
---------
On each day, scan every black tile and its neighbours.  Tally neighbour
counts in a dict, then apply the rules to produce the next generation.
"""

from collections import defaultdict
from pathlib import Path

from day24 import HEX_DIRS, identify_black_tiles


def step(black: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """Advance the hex-grid automaton by one day."""
    neighbour_count: dict[tuple[int, int], int] = defaultdict(int)
    for q, r in black:
        for dq, dr in HEX_DIRS.values():
            neighbour_count[(q + dq, r + dr)] += 1

    new_black: set[tuple[int, int]] = set()
    for tile in black:
        c = neighbour_count.get(tile, 0)
        if 1 <= c <= 2:
            new_black.add(tile)
    for tile, c in neighbour_count.items():
        if tile not in black and c == 2:
            new_black.add(tile)
    return new_black


def simulate(black: set[tuple[int, int]], days: int) -> set[tuple[int, int]]:
    """Run the hex Game of Life for *days* generations."""
    for _ in range(days):
        black = step(black)
    return black


def solve(input_path: str = "advent2020/Day24/d24_input.txt") -> int:
    """Read input, flip tiles, run 100 days, return black tile count."""
    lines = [
        ln for ln in Path(input_path).read_text().splitlines() if ln.strip()
    ]
    black = identify_black_tiles(lines)
    black = simulate(black, 100)
    return len(black)


if __name__ == "__main__":
    result = solve()
    print(f"Black tiles after 100 days: {result}")
