#!/usr/bin/env python3
"""Tests for Day 25 using the example from the problem statement.

2 locks and 3 keys. 3 lock/key pairs fit without overlap.
Part 2 is the free star; just prints "Merry Christmas!".
"""

from day25 import solve as solve_p1
from day25_part2 import solve as solve_p2

EXAMPLE = """\
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
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
    assert solve_p1(EXAMPLE) == 3


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
    assert solve_p2(EXAMPLE) == "Merry Christmas!"


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 3")
    test_part2()
    print("PASS  Part 2: Merry Christmas!")
    print("\nAll Day 25 tests passed!")
