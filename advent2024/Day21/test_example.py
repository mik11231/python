#!/usr/bin/env python3
"""Tests for Day 21 using the example from the problem statement.

Five codes: 029A, 980A, 179A, 456A, 379A.
Part 1 (2 robots): complexities 68*29 + 60*980 + 68*179 + 64*456 + 64*379 = 126384.
Part 2 (25 robots): just verify it produces a positive integer.
"""

from day21 import solve as solve_p1
from day21_part2 import solve as solve_p2

EXAMPLE = """\
029A
980A
179A
456A
379A
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
    assert solve_p1(EXAMPLE) == 126384


def test_part2_runs():
    """
    Run `test_part2_runs` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    result = solve_p2(EXAMPLE)
    assert result > 0


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 126384")
    test_part2_runs()
    print("PASS  Part 2: runs OK")
    print("\nAll Day 21 tests passed!")
