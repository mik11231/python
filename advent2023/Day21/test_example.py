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
    """
    Run `test_part1` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p1(EXAMPLE, steps=6) == 16


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 16")
    print("\nAll Day 21 tests passed!")
