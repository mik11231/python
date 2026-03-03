#!/usr/bin/env python3
"""Tests for Day 23 using the example from the problem statement.

Starting cups: 389125467
Part 1 (100 moves): labels after cup 1 = "67384529"
Part 2 (10M moves, 1M cups): two cups after 1 are 934001 and 159792.
         Product = 149245887792.
"""

from day23 import play_cups, labels_after_one
from day23_part2 import play_cups_extended

STARTING = "389125467"


def test_10_moves():
    """Verify labels after cup 1 are 92658374 after 10 moves."""
    nxt = play_cups(STARTING, 10)
    result = labels_after_one(nxt)
    assert result == "92658374", f"After 10 moves expected 92658374, got {result}"
    print(f"PASS  10 moves: {result}")


def test_part1():
    """Verify Part 1 example: labels after cup 1 are 67384529 after 100 moves."""
    nxt = play_cups(STARTING, 100)
    result = labels_after_one(nxt)
    assert result == "67384529", f"Expected 67384529, got {result}"
    print(f"PASS  Part 1 (100 moves): {result}")


def test_part2():
    """Verify Part 2 example: product of two cups after 1 is 149245887792."""
    nxt = play_cups_extended(STARTING)
    a = nxt[1]
    b = nxt[a]
    assert a == 934001, f"Expected first cup 934001, got {a}"
    assert b == 159792, f"Expected second cup 159792, got {b}"
    product = a * b
    assert product == 149245887792, f"Expected 149245887792, got {product}"
    print(f"PASS  Part 2: {a} * {b} = {product}")


if __name__ == "__main__":
    test_10_moves()
    test_part1()
    test_part2()
    print("\nAll Day 23 tests passed!")
