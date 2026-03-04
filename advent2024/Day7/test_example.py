#!/usr/bin/env python3
"""Tests for Day 7 using the example from the problem statement.

9 equations; with + and * only, 3 are achievable (sum 3749).
With + , *, and ||, 6 are achievable (sum 11387).
"""

from day7 import solve as solve_p1
from day7_part2 import solve as solve_p2

EXAMPLE = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
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
    assert solve_p1(EXAMPLE) == 3749


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
    assert solve_p2(EXAMPLE) == 11387


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 3749")
    test_part2()
    print("PASS  Part 2: 11387")
    print("\nAll Day 7 tests passed!")
