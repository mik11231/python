#!/usr/bin/env python3
"""Tests for Day 13 using the example from the problem statement.

Pattern 1: vertical reflection at column 5 => 5
Pattern 2: horizontal reflection at row 4 => 400
Part 1 total: 405
Part 2 total: 400
"""

from day13 import solve as solve_p1
from day13_part2 import solve as solve_p2

EXAMPLE = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
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
    assert solve_p1(EXAMPLE) == 405


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
    assert solve_p2(EXAMPLE) == 400


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 405")
    test_part2()
    print("PASS  Part 2: 400")
    print("\nAll Day 13 tests passed!")
