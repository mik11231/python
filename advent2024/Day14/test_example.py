#!/usr/bin/env python3
"""Tests for Day 14 using the example from the problem statement.

12 robots on an 11x7 grid. After 100 seconds the quadrant counts are
1, 3, 4, 1 giving a safety factor of 12.
"""

from day14 import solve as solve_p1

EXAMPLE = """\
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


def test_part1():
    assert solve_p1(EXAMPLE, width=11, height=7, steps=100) == 12


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: safety factor = 12")
    print("\nAll Day 14 tests passed!")
