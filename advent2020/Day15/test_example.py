#!/usr/bin/env python3
"""Tests for Day 15: Rambunctious Recitation using the provided examples."""

from day15 import play_game


def test_sequence_0_3_6():
    """The worked example: starting with 0,3,6 the sequence is
    0, 3, 6, 0, 3, 3, 1, 0, 4, 0 and the 2020th number is 436."""
    starting = [0, 3, 6]

    assert play_game(starting, 4) == 0
    assert play_game(starting, 5) == 3
    assert play_game(starting, 6) == 3
    assert play_game(starting, 7) == 1
    assert play_game(starting, 8) == 0
    assert play_game(starting, 9) == 4
    assert play_game(starting, 10) == 0

    assert play_game(starting, 2020) == 436


def test_additional_part1_cases():
    """Verify Part 1 2020th number for various starting sequences."""
    cases = [
        ([1, 3, 2], 1),
        ([2, 1, 3], 10),
        ([1, 2, 3], 27),
        ([2, 3, 1], 78),
        ([3, 2, 1], 438),
        ([3, 1, 2], 1836),
    ]
    for starting, expected in cases:
        result = play_game(starting, 2020)
        assert result == expected, (
            f"Starting {starting}: expected {expected}, got {result}"
        )


if __name__ == "__main__":
    test_sequence_0_3_6()
    test_additional_part1_cases()
    print("All Day 15 tests passed.")
