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
    assert solve_p1(EXAMPLE) == 374


def test_expansion_10():
    assert galaxy_distances(EXAMPLE, expansion=10) == 1030


def test_expansion_100():
    assert galaxy_distances(EXAMPLE, expansion=100) == 8410


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1 (expansion=2): 374")
    test_expansion_10()
    print("PASS  Expansion=10: 1030")
    test_expansion_100()
    print("PASS  Expansion=100: 8410")
    print("\nAll Day 11 tests passed!")
