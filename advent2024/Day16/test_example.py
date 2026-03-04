#!/usr/bin/env python3
"""Tests for Day 16 using examples from the problem statement.

Example 1: 15x15 maze, best score = 7036, tiles on best paths = 45.
Example 2: 17x17 maze, best score = 11048, tiles on best paths = 64.
"""

from day16 import solve as solve_p1
from day16_part2 import solve as solve_p2

EXAMPLE1 = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

EXAMPLE2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""


def test_part1_ex1():
    assert solve_p1(EXAMPLE1) == 7036


def test_part1_ex2():
    assert solve_p1(EXAMPLE2) == 11048


def test_part2_ex1():
    assert solve_p2(EXAMPLE1) == 45


def test_part2_ex2():
    assert solve_p2(EXAMPLE2) == 64


if __name__ == "__main__":
    test_part1_ex1()
    print("PASS  Part 1 example 1: 7036")
    test_part1_ex2()
    print("PASS  Part 1 example 2: 11048")
    test_part2_ex1()
    print("PASS  Part 2 example 1: 45")
    test_part2_ex2()
    print("PASS  Part 2 example 2: 64")
    print("\nAll Day 16 tests passed!")
