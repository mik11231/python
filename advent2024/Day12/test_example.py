#!/usr/bin/env python3
"""Tests for Day 12 using examples from the problem statement.

Small 4x4 map: Part 1 = 140, Part 2 = 80.
Larger 10x10 map: Part 1 = 1930, Part 2 = 1206.
"""

from day12 import solve as solve_p1
from day12_part2 import solve as solve_p2

SMALL = """\
AAAA
BBCD
BBCC
EEEC
"""

LARGE = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""


def test_part1_small():
    """
    Run `test_part1_small` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p1(SMALL) == 140


def test_part1_large():
    """
    Run `test_part1_large` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p1(LARGE) == 1930


def test_part2_small():
    """
    Run `test_part2_small` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p2(SMALL) == 80


def test_part2_large():
    """
    Run `test_part2_large` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p2(LARGE) == 1206


if __name__ == "__main__":
    test_part1_small()
    print("PASS  Part 1 small: 140")
    test_part1_large()
    print("PASS  Part 1 large: 1930")
    test_part2_small()
    print("PASS  Part 2 small: 80")
    test_part2_large()
    print("PASS  Part 2 large: 1206")
    print("\nAll Day 12 tests passed!")
