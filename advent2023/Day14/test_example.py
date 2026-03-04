#!/usr/bin/env python3
"""Tests for Day 14 using the example from the problem statement.

Tilt north: total load = 136
Spin cycle 1 billion times: total load = 64
"""

from day14 import solve as solve_p1
from day14_part2 import solve as solve_p2

EXAMPLE = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 136


def test_part2():
    assert solve_p2(EXAMPLE) == 64


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 136")
    test_part2()
    print("PASS  Part 2: 64")
    print("\nAll Day 14 tests passed!")
