#!/usr/bin/env python3
"""Tests for Day 8 using the examples from the problem statement."""

from day8 import solve as solve_p1
from day8_part2 import solve as solve_p2

EXAMPLE1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

EXAMPLE2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

EXAMPLE_P2 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


def test_part1_example1():
    assert solve_p1(EXAMPLE1) == 2


def test_part1_example2():
    assert solve_p1(EXAMPLE2) == 6


def test_part2():
    assert solve_p2(EXAMPLE_P2) == 6


if __name__ == "__main__":
    test_part1_example1()
    print("PASS  Part 1 example 1: 2 steps")
    test_part1_example2()
    print("PASS  Part 1 example 2: 6 steps")
    test_part2()
    print("PASS  Part 2: 6 steps")
    print("\nAll Day 8 tests passed!")
