#!/usr/bin/env python3
"""Tests for Day 9 using the example from the problem statement.

Example histories:
    0 3 6 9 12 15  -> next=18, prev=-3
    1 3 6 10 15 21 -> next=28, prev=0
    10 13 16 21 30 45 -> next=68, prev=5
Part 1 sum of nexts: 114
Part 2 sum of prevs: 2
"""

from day9 import solve as solve_p1
from day9_part2 import solve as solve_p2

EXAMPLE = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
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
    assert solve_p1(EXAMPLE) == 114


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
    assert solve_p2(EXAMPLE) == 2


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 114")
    test_part2()
    print("PASS  Part 2: 2")
    print("\nAll Day 9 tests passed!")
