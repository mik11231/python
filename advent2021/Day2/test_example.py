#!/usr/bin/env python3
"""Tests for Day 2 using the example from the problem statement.

Example commands:
    forward 5, down 5, forward 8, up 3, down 8, forward 2

Part 1: horizontal=15, depth=10  -> 150
Part 2: horizontal=15, depth=60  -> 900
"""

from day2 import parse_commands, navigate
from day2_part2 import navigate_with_aim

EXAMPLE_TEXT = """\
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""

COMMANDS = parse_commands(EXAMPLE_TEXT)


def test_part1():
    """Verify Part 1: simple navigation gives product 150."""
    h, d = navigate(COMMANDS)
    assert h == 15 and d == 10, f"Expected (15, 10), got ({h}, {d})"
    assert h * d == 150


def test_part2():
    """Verify Part 2: aim-based navigation gives product 900."""
    h, d = navigate_with_aim(COMMANDS)
    assert h == 15 and d == 60, f"Expected (15, 60), got ({h}, {d})"
    assert h * d == 900


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 150")
    test_part2()
    print("PASS  Part 2: 900")
    print("\nAll Day 2 tests passed!")
