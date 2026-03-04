#!/usr/bin/env python3
"""Tests for Day 18 using the example from the problem statement.

7x7 grid (size=7), first 12 bytes. Shortest path = 22.
First blocking byte = 6,1 (the 21st byte, index 20).
"""

from day18 import solve as solve_p1
from day18_part2 import solve as solve_p2

EXAMPLE = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


def test_part1():
    assert solve_p1(EXAMPLE, size=7, n_bytes=12) == 22


def test_part2():
    assert solve_p2(EXAMPLE, size=7) == "6,1"


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 22 steps")
    test_part2()
    print("PASS  Part 2: 6,1")
    print("\nAll Day 18 tests passed!")
