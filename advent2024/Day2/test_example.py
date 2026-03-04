#!/usr/bin/env python3
"""Tests for Day 2 using the example from the problem statement.

Example reports: 7 6 4 2 1 / 1 2 7 8 9 / 9 7 6 2 1 / 1 3 2 4 5 / 8 6 4 4 1 / 1 3 6 7 9

Part 1: 2 safe reports
Part 2: 4 safe reports (with Problem Dampener)
"""

from day2 import solve as solve_p1
from day2_part2 import solve as solve_p2

EXAMPLE = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
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
    assert solve_p1(EXAMPLE) == 2


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
    assert solve_p2(EXAMPLE) == 4


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 2 safe reports")
    test_part2()
    print("PASS  Part 2: 4 safe reports")
    print("\nAll Day 2 tests passed!")
