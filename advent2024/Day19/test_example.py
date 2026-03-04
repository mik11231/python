#!/usr/bin/env python3
"""Tests for Day 19 using the example from the problem statement.

8 designs with patterns r, wr, b, g, bwu, rb, gb, br.
6 designs are possible (Part 1). Total ways = 16 (Part 2).
"""

from day19 import solve as solve_p1
from day19_part2 import solve as solve_p2

EXAMPLE = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 6


def test_part2():
    assert solve_p2(EXAMPLE) == 16


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 6 designs possible")
    test_part2()
    print("PASS  Part 2: 16 total ways")
    print("\nAll Day 19 tests passed!")
