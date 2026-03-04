#!/usr/bin/env python3
"""Tests for Day 5 using the example from the problem statement.

21 ordering rules + 6 updates.
Part 1: correctly ordered updates have middle pages 61+53+29 = 143
Part 2: fixed incorrect updates have middle pages 47+29+47 = 123
"""

from day5 import solve as solve_p1
from day5_part2 import solve as solve_p2

EXAMPLE = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 143


def test_part2():
    assert solve_p2(EXAMPLE) == 123


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 143")
    test_part2()
    print("PASS  Part 2: 123")
    print("\nAll Day 5 tests passed!")
