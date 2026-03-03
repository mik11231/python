#!/usr/bin/env python3
"""Tests for Day 10 using both examples from the problem statement.

Small example:
    16 10 15 5 1 11 7 19 6 12 4
    -> 7 one-jolt diffs, 5 three-jolt diffs -> 7 * 5 = 35
    -> 8 distinct arrangements

Large example:
    28 33 18 42 31 14 46 20 48 47 24 23 49 45 19 38 39 11 1 32 25 35 8 17 7 9 4 2 34 10 3
    -> 22 one-jolt diffs, 10 three-jolt diffs -> 22 * 10 = 220
    -> 19208 distinct arrangements
"""

from day10 import parse_adapters, count_differences
from day10_part2 import count_arrangements

SMALL = "16\n10\n15\n5\n1\n11\n7\n19\n6\n12\n4"
LARGE = "28\n33\n18\n42\n31\n14\n46\n20\n48\n47\n24\n23\n49\n45\n19\n38\n39\n11\n1\n32\n25\n35\n8\n17\n7\n9\n4\n2\n34\n10\n3"


def test_part1_small():
    """Verify Part 1 small example: 1-jolt × 3-jolt diffs = 35."""
    adapters = parse_adapters(SMALL)
    diffs = count_differences(adapters)
    product = diffs[1] * diffs[3]
    assert product == 35, f"Expected 35, got {product}"
    print(f"PASS  Part 1 (small): {diffs[1]}×{diffs[3]} = {product}")


def test_part1_large():
    """Verify Part 1 large example: 1-jolt × 3-jolt diffs = 220."""
    adapters = parse_adapters(LARGE)
    diffs = count_differences(adapters)
    product = diffs[1] * diffs[3]
    assert product == 220, f"Expected 220, got {product}"
    print(f"PASS  Part 1 (large): {diffs[1]}×{diffs[3]} = {product}")


def test_part2_small():
    """Verify Part 2 small example: 8 distinct adapter arrangements."""
    adapters = parse_adapters(SMALL)
    result = count_arrangements(adapters)
    assert result == 8, f"Expected 8, got {result}"
    print(f"PASS  Part 2 (small): {result} arrangements")


def test_part2_large():
    """Verify Part 2 large example: 19208 distinct adapter arrangements."""
    adapters = parse_adapters(LARGE)
    result = count_arrangements(adapters)
    assert result == 19208, f"Expected 19208, got {result}"
    print(f"PASS  Part 2 (large): {result} arrangements")


if __name__ == "__main__":
    test_part1_small()
    test_part1_large()
    test_part2_small()
    test_part2_large()
    print("\nAll Day 10 tests passed!")
