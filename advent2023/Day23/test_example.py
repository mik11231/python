#!/usr/bin/env python3
"""Tests for Day 23 using the example from the problem statement.

Example: 23x23 hiking trail. Part 1 (with slopes): 94. Part 2 (ignore slopes): 154.
"""

from day23 import solve as solve_p1
from day23_part2 import solve as solve_p2

EXAMPLE = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 94


def test_part2():
    assert solve_p2(EXAMPLE) == 154


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 94")
    test_part2()
    print("PASS  Part 2: 154")
    print("\nAll Day 23 tests passed!")
