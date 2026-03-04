#!/usr/bin/env python3
"""Tests for Day 8 using the example from the problem statement.

12x12 grid with '0' and 'A' antennas.
Part 1: 14 unique antinode locations.  Part 2: 34 collinear antinode locations.
"""

from day8 import solve as solve_p1
from day8_part2 import solve as solve_p2

EXAMPLE = """\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
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
    assert solve_p1(EXAMPLE) == 14


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
    assert solve_p2(EXAMPLE) == 34


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 14")
    test_part2()
    print("PASS  Part 2: 34")
    print("\nAll Day 8 tests passed!")
