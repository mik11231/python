#!/usr/bin/env python3
"""Tests for Day 4 using the example from the problem statement.

10x10 grid where XMAS appears 18 times (Part 1) and X-MAS appears 9 times (Part 2).
"""

from day4 import solve as solve_p1
from day4_part2 import solve as solve_p2

EXAMPLE = """\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
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
    assert solve_p1(EXAMPLE) == 18


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
    assert solve_p2(EXAMPLE) == 9


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 18 XMAS occurrences")
    test_part2()
    print("PASS  Part 2: 9 X-MAS patterns")
    print("\nAll Day 4 tests passed!")
