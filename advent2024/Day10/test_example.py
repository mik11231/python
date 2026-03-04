#!/usr/bin/env python3
"""Tests for Day 10 using the larger example from the problem statement.

8x8 topographic map with 9 trailheads.
Part 1: sum of scores = 36.  Part 2: sum of ratings = 81.
"""

from day10 import solve as solve_p1
from day10_part2 import solve as solve_p2

EXAMPLE = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
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
    assert solve_p1(EXAMPLE) == 36


def test_part2():
    """
    Run `test_part2` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p2(EXAMPLE) == 81


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 36")
    test_part2()
    print("PASS  Part 2: 81")
    print("\nAll Day 10 tests passed!")
