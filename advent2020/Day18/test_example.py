#!/usr/bin/env python3
"""Tests for Day 18: Operation Order using the puzzle examples."""

from day18 import evaluate
from day18_part2 import ADDITION_FIRST

PART1_CASES = [
    ("1 + 2 * 3 + 4 * 5 + 6", 71),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 26),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
]

PART2_CASES = [
    ("1 + 2 * 3 + 4 * 5 + 6", 231),
    ("1 + (2 * 3) + (4 * (5 + 6))", 51),
    ("2 * 3 + (4 * 5)", 46),
    ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 1445),
    ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 669060),
    ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 23340),
]


def test_part1_examples() -> None:
    """Verify Part 1 left-to-right expression evaluation for all examples."""
    for expr, expected in PART1_CASES:
        result = evaluate(expr)
        assert result == expected, f"Part 1: {expr!r} -> {result}, expected {expected}"


def test_part2_examples() -> None:
    """Verify Part 2 addition-first expression evaluation for all examples."""
    for expr, expected in PART2_CASES:
        result = evaluate(expr, ADDITION_FIRST)
        assert result == expected, f"Part 2: {expr!r} -> {result}, expected {expected}"


if __name__ == "__main__":
    test_part1_examples()
    test_part2_examples()
    print("All Day 18 tests passed!")
