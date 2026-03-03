#!/usr/bin/env python3
"""Tests for Day 9 using the example from the problem statement.

Example (preamble = 5):
    35 20 15 25 47 40 62 55 65 95 102 117 150 182 127 219 299 277 309 576

Part 1: 127 is the first number that is NOT a sum of two of the preceding 5.
Part 2: The contiguous range [15, 25, 47, 40] sums to 127.
        Answer = min(15,25,47,40) + max(15,25,47,40) = 15 + 47 = 62.
"""

from day9 import find_invalid
from day9_part2 import find_contiguous_range

EXAMPLE = [35, 20, 15, 25, 47, 40, 62, 55, 65, 95,
           102, 117, 150, 182, 127, 219, 299, 277, 309, 576]


def test_part1():
    """Verify Part 1 example: first invalid number is 127."""
    result = find_invalid(EXAMPLE, preamble=5)
    assert result == 127, f"Expected 127, got {result}"
    print(f"PASS  Part 1: first invalid number = {result}")


def test_part2():
    """Verify Part 2 example: contiguous range sums to 127, min+max = 62."""
    rng = find_contiguous_range(EXAMPLE, 127)
    assert sum(rng) == 127, f"Range should sum to 127, got {sum(rng)}"
    answer = min(rng) + max(rng)
    assert answer == 62, f"Expected 62, got {answer}"
    print(f"PASS  Part 2: min + max of range = {answer}")


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("\nAll Day 9 tests passed!")
