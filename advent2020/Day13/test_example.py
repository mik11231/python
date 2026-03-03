#!/usr/bin/env python3
"""Tests for Day 13: Shuttle Search using the provided examples."""

from day13 import parse_input, earliest_bus, parse_input_with_offsets
from day13_part2 import find_earliest_timestamp

EXAMPLE = """\
939
7,13,x,x,59,x,31,19
"""


def test_part1_example():
    """Verify Part 1 example: bus 59 departs in 5 minutes, product 295."""
    timestamp, buses = parse_input(EXAMPLE)
    bus_id, wait = earliest_bus(timestamp, buses)
    assert bus_id == 59, f"Expected bus 59, got {bus_id}"
    assert wait == 5, f"Expected wait 5, got {wait}"
    assert bus_id * wait == 295


def test_part2_main_example():
    """Verify Part 2 main example: earliest timestamp is 1068781."""
    buses = parse_input_with_offsets(EXAMPLE)
    assert find_earliest_timestamp(buses) == 1068781


def test_part2_additional_examples():
    """Verify Part 2 additional bus schedule examples."""
    cases = [
        ("17,x,13,19", 3417),
        ("67,7,59,61", 754018),
        ("67,x,7,59,61", 779210),
        ("67,7,x,59,61", 1261476),
        ("1789,37,47,1889", 1202161486),
    ]
    for schedule, expected in cases:
        text = f"0\n{schedule}\n"
        buses = parse_input_with_offsets(text)
        result = find_earliest_timestamp(buses)
        assert result == expected, f"For {schedule}: expected {expected}, got {result}"


if __name__ == "__main__":
    test_part1_example()
    test_part2_main_example()
    test_part2_additional_examples()
    print("All Day 13 tests passed.")
