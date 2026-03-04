#!/usr/bin/env python3
"""Tests for Day 11 using the example from the problem statement.

Part 1 (expansion=2): 374
Expansion=10: 1030
Expansion=100: 8410
"""

from day11 import galaxy_distances, solve as solve_p1

EXAMPLE = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
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
    assert solve_p1(EXAMPLE) == 374


def test_expansion_10():
    """
    Run `test_expansion_10` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert galaxy_distances(EXAMPLE, expansion=10) == 1030


def test_expansion_100():
    """
    Run `test_expansion_100` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: none.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    assert galaxy_distances(EXAMPLE, expansion=100) == 8410


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1 (expansion=2): 374")
    test_expansion_10()
    print("PASS  Expansion=10: 1030")
    test_expansion_100()
    print("PASS  Expansion=100: 8410")
    print("\nAll Day 11 tests passed!")
