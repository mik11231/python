#!/usr/bin/env python3
"""Tests for Day 22 using the example from the problem statement.

Example: 7 bricks. Part 1: 5 safely removable. Part 2: 7 total would fall.
"""

from day22 import solve as solve_p1
from day22_part2 import solve as solve_p2

EXAMPLE = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 5


def test_part2():
    assert solve_p2(EXAMPLE) == 7


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 5")
    test_part2()
    print("PASS  Part 2: 7")
    print("\nAll Day 22 tests passed!")
