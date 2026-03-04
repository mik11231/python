#!/usr/bin/env python3
"""Tests for Day 20 using the example from the problem statement.

The example grid has 44 cheats total (2-step), and specific counts per saving.
With threshold=20 for part 1, there are 5 cheats (save 20,36,38,40,64).
For part 2, threshold=50: cheats saving >=50 picoseconds.
"""

from day20 import solve as solve_p1
from day20_part2 import solve as solve_p2

EXAMPLE = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
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
    assert solve_p1(EXAMPLE, threshold=20) == 5


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
    assert solve_p2(EXAMPLE, threshold=50) == 285


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 5 cheats saving >= 20")
    test_part2()
    print("PASS  Part 2: 285 cheats saving >= 50")
    print("\nAll Day 20 tests passed!")
