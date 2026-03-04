#!/usr/bin/env python3
"""Tests for Day 10 using the examples from the problem statement."""

from day10 import solve as solve_p1
from day10_part2 import solve as solve_p2

SIMPLE = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""

COMPLEX = """\
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
"""

ENCLOSED_SIMPLE = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""

ENCLOSED_COMPLEX = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7.
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""


def test_part1_simple():
    """
    Run `test_part1_simple` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p1(SIMPLE) == 4


def test_part1_complex():
    """
    Run `test_part1_complex` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p1(COMPLEX) == 8


def test_part2_simple():
    """
    Run `test_part2_simple` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p2(ENCLOSED_SIMPLE) == 4


def test_part2_complex():
    """
    Run `test_part2_complex` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert solve_p2(ENCLOSED_COMPLEX) == 8


if __name__ == "__main__":
    test_part1_simple()
    print("PASS  Part 1 simple: 4")
    test_part1_complex()
    print("PASS  Part 1 complex: 8")
    test_part2_simple()
    print("PASS  Part 2 simple enclosed: 4")
    test_part2_complex()
    print("PASS  Part 2 complex enclosed: 8")
    print("\nAll Day 10 tests passed!")
