#!/usr/bin/env python3
"""Tests for Day 16 using the example from the problem statement.

Beam from top-left heading right energizes 46 tiles.
Best starting position energizes 51 tiles.
"""

from day16 import solve as solve_p1
from day16_part2 import solve as solve_p2

EXAMPLE = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
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
    assert solve_p1(EXAMPLE) == 46


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
    assert solve_p2(EXAMPLE) == 51


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 46")
    test_part2()
    print("PASS  Part 2: 51")
    print("\nAll Day 16 tests passed!")
