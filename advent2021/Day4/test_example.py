#!/usr/bin/env python3
"""Tests for Day 4 using the example from the problem statement.

Drawn numbers:
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

Three 5×5 boards (see EXAMPLE_TEXT below).

Part 1: Board 3 wins first when 24 is called; score = 4512
Part 2: Board 2 wins last  when 13 is called; score = 1924
"""

from day4 import parse_bingo, play_bingo
from day4_part2 import play_bingo_last

EXAMPLE_TEXT = """\
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""


def test_part1():
    """Verify Part 1: first winning board scores 4512."""
    numbers, boards = parse_bingo(EXAMPLE_TEXT)
    _, score = play_bingo(numbers, boards)
    assert score == 4512, f"Expected 4512, got {score}"


def test_part2():
    """Verify Part 2: last winning board scores 1924."""
    numbers, boards = parse_bingo(EXAMPLE_TEXT)
    _, score = play_bingo_last(numbers, boards)
    assert score == 1924, f"Expected 1924, got {score}"


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 4512")
    test_part2()
    print("PASS  Part 2: 1924")
    print("\nAll Day 4 tests passed!")
