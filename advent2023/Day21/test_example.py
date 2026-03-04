#!/usr/bin/env python3
"""Tests for Day 21 using the example from the problem statement.

Example: 11x11 garden grid, 6 steps => 16 reachable plots.
Part 2 uses quadratic extrapolation specific to full input dimensions.
"""

from day21 import solve as solve_p1

EXAMPLE = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def test_part1():
    assert solve_p1(EXAMPLE, steps=6) == 16


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 16")
    print("\nAll Day 21 tests passed!")
