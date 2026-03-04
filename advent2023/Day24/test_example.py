#!/usr/bin/env python3
"""Tests for Day 24 using the example from the problem statement.

Example: 5 hailstones. Part 1 (test area 7-27): 2 intersections.
Part 2: rock position sum = 47.
"""

from day24 import solve as solve_p1
from day24_part2 import solve as solve_p2

EXAMPLE = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
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
    assert solve_p1(EXAMPLE, lo=7, hi=27) == 2


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
    assert solve_p2(EXAMPLE) == 47


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 2")
    test_part2()
    print("PASS  Part 2: 47")
    print("\nAll Day 24 tests passed!")
