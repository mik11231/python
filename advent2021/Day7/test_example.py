#!/usr/bin/env python3
"""Tests for Day 7 using the example from the problem statement.

Example positions: 16,1,2,0,4,2,7,1,2,14

Part 1 (linear cost):     position 2, fuel  37
Part 2 (triangular cost): position 5, fuel 168
"""

from day7 import min_fuel_linear
from day7_part2 import min_fuel_triangular

EXAMPLE = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def test_part1():
    """Verify Part 1: optimal position 2, total fuel 37."""
    pos, fuel = min_fuel_linear(EXAMPLE)
    assert pos == 2, f"Expected position 2, got {pos}"
    assert fuel == 37, f"Expected fuel 37, got {fuel}"


def test_part2():
    """Verify Part 2: optimal position 5, total fuel 168."""
    pos, fuel = min_fuel_triangular(EXAMPLE)
    assert pos == 5, f"Expected position 5, got {pos}"
    assert fuel == 168, f"Expected fuel 168, got {fuel}"


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: position 2, fuel 37")
    test_part2()
    print("PASS  Part 2: position 5, fuel 168")
    print("\nAll Day 7 tests passed!")
