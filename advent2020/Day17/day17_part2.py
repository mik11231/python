#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 17: Conway Cubes (Part 2)

Same rules as Part 1 but in four dimensions (x, y, z, w).

Algorithm
---------
Reuse Part 1's `simulate` and `parse_initial_state` with dimensions=4.
The neighbor generation and counting are dimension-agnostic.
"""

from pathlib import Path

from day17 import parse_initial_state, simulate


def solve(input_path: str = "advent2020/Day17/d17_input.txt") -> int:
    """Return the number of active hypercubes after 6 cycles in 4-D."""
    text = Path(input_path).read_text()
    initial = parse_initial_state(text, dimensions=4)
    final = simulate(initial, dimensions=4, cycles=6)
    return len(final)


if __name__ == "__main__":
    result = solve()
    print(f"Active cubes after 6 cycles (4D): {result}")
