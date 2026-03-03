#!/usr/bin/env python3
"""Tests for Day 12: Rain Risk using the provided example."""

from day12 import parse_instructions, navigate
from day12_part2 import navigate_waypoint

EXAMPLE = """\
F10
N3
F7
R90
F11
"""


def test_part1_example():
    """Verify Part 1 example: Manhattan distance after navigation is 25."""
    instructions = parse_instructions(EXAMPLE)
    x, y = navigate(instructions)
    assert (x, y) == (17, -8), f"Expected (17, -8), got ({x}, {y})"
    assert abs(x) + abs(y) == 25


def test_part2_example():
    """Verify Part 2 example: Manhattan distance with waypoint navigation is 286."""
    instructions = parse_instructions(EXAMPLE)
    x, y = navigate_waypoint(instructions)
    assert abs(x) + abs(y) == 286, f"Expected 286, got {abs(x) + abs(y)}"


if __name__ == "__main__":
    test_part1_example()
    test_part2_example()
    print("All Day 12 tests passed.")
