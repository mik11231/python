#!/usr/bin/env python3
"""Tests for Day 20 using examples from the problem statement.

Example 1: broadcaster -> a, b, c with inverter loop => 32000000
Example 2: broadcaster -> a with dual flip-flops => 11687500
Part 2 is not testable with examples (requires 'rx' module).
"""

from day20 import solve as solve_p1

EXAMPLE1 = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""

EXAMPLE2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


def test_part1_example1():
    assert solve_p1(EXAMPLE1) == 32000000


def test_part1_example2():
    assert solve_p1(EXAMPLE2) == 11687500


if __name__ == "__main__":
    test_part1_example1()
    print("PASS  Part 1 Example 1: 32000000")
    test_part1_example2()
    print("PASS  Part 1 Example 2: 11687500")
    print("\nAll Day 20 tests passed!")
