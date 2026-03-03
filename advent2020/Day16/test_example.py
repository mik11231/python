#!/usr/bin/env python3
"""Tests for Day 16: Ticket Translation using the puzzle examples."""

from day16 import get_invalid_values, parse_input
from day16_part2 import determine_field_positions

EXAMPLE_PART1 = """\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
"""

EXAMPLE_PART2 = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
"""


def test_parse_input() -> None:
    """Verify parsing yields 3 rules, your ticket, and 4 nearby tickets."""
    rules, your_ticket, nearby = parse_input(EXAMPLE_PART1)
    assert len(rules) == 3
    assert your_ticket == [7, 1, 14]
    assert len(nearby) == 4


def test_invalid_values() -> None:
    """Verify invalid ticket values are 4, 12, and 55."""
    rules, _, nearby = parse_input(EXAMPLE_PART1)
    all_invalid = [v for t in nearby for v in get_invalid_values(rules, t)]
    assert sorted(all_invalid) == [4, 12, 55]


def test_error_rate() -> None:
    """Verify Part 1 error rate (sum of invalid values) is 71."""
    rules, _, nearby = parse_input(EXAMPLE_PART1)
    error_rate = sum(v for t in nearby for v in get_invalid_values(rules, t))
    assert error_rate == 71


def test_field_assignment() -> None:
    """Verify Part 2 field-to-position mapping for row, class, seat."""
    rules, _, nearby = parse_input(EXAMPLE_PART2)
    valid_tickets = [t for t in nearby if not get_invalid_values(rules, t)]
    mapping = determine_field_positions(rules, valid_tickets)
    assert mapping["row"] == 0
    assert mapping["class"] == 1
    assert mapping["seat"] == 2


if __name__ == "__main__":
    test_parse_input()
    test_invalid_values()
    test_error_rate()
    test_field_assignment()
    print("All Day 16 tests passed!")
