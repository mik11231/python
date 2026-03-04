#!/usr/bin/env python3
"""Tests for Day 6 using the example from the problem statement.

10x10 grid with guard starting at (6,4) facing up.
Part 1: guard visits 41 distinct positions.
Part 2: 6 positions where a new obstacle creates a loop.
"""

from day6 import solve as solve_p1
from day6_part2 import solve as solve_p2

EXAMPLE = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
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
    assert solve_p1(EXAMPLE) == 41


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
    assert solve_p2(EXAMPLE) == 6


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 41 positions visited")
    test_part2()
    print("PASS  Part 2: 6 loop-creating positions")
    print("\nAll Day 6 tests passed!")
