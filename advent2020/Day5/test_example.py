#!/usr/bin/env python3
"""Tests for Day 5 using the examples from the problem statement.

Example boarding passes and their seat IDs:
    FBFBBFFRLR  ->  row 44, col 5, ID 357
    BFFFBBFRRR  ->  row 70, col 7, ID 567
    FFFBBBFRRR  ->  row 14, col 7, ID 119
    BBFFBBFRLL  ->  row 102, col 4, ID 820
"""

from day5 import seat_id

EXAMPLES = [
    ("FBFBBFFRLR", 44, 5, 357),
    ("BFFFBBFRRR", 70, 7, 567),
    ("FFFBBBFRRR", 14, 7, 119),
    ("BBFFBBFRLL", 102, 4, 820),
]


def test_seat_ids():
    """Verify all example boarding passes compute correct row, col, and seat ID."""
    for boarding_pass, expected_row, expected_col, expected_id in EXAMPLES:
        sid = seat_id(boarding_pass)
        row = sid // 8
        col = sid % 8
        assert row == expected_row, f"{boarding_pass}: row {row} != {expected_row}"
        assert col == expected_col, f"{boarding_pass}: col {col} != {expected_col}"
        assert sid == expected_id, f"{boarding_pass}: id {sid} != {expected_id}"
        print(f"PASS  {boarding_pass}  row={row} col={col} id={sid}")


def test_highest():
    """Verify highest seat ID from examples is 820."""
    ids = [seat_id(bp) for bp, *_ in EXAMPLES]
    assert max(ids) == 820, f"Expected highest ID 820, got {max(ids)}"
    print(f"PASS  Highest seat ID: {max(ids)}")


if __name__ == "__main__":
    test_seat_ids()
    test_highest()
    print("\nAll Day 5 tests passed!")
