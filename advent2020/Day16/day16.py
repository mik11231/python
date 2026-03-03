#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 16: Ticket Translation (Part 1)

The train ticket has fields in an unknown order.  The input has three sections:
field validation rules (each with two valid ranges), your ticket, and nearby
tickets.  A value is invalid if it does not satisfy ANY rule.

Algorithm
---------
1. Parse the three input sections with a regex for the rules.
2. Build a set of all individually-valid integers across every rule.
3. For each value on every nearby ticket, check membership in that set.
4. Sum the invalid values (the "ticket scanning error rate").
"""

import re
from pathlib import Path


def parse_input(text: str) -> tuple[dict[str, list[tuple[int, int]]], list[int], list[list[int]]]:
    """Parse the puzzle input into (rules, your_ticket, nearby_tickets).

    *rules* maps field name -> list of (lo, hi) inclusive ranges.
    """
    sections = text.strip().split("\n\n")
    rules: dict[str, list[tuple[int, int]]] = {}
    for line in sections[0].splitlines():
        m = re.match(r"(.+?):\s*(\d+)-(\d+)\s+or\s+(\d+)-(\d+)", line)
        if m:
            name = m.group(1)
            rules[name] = [
                (int(m.group(2)), int(m.group(3))),
                (int(m.group(4)), int(m.group(5))),
            ]

    your_ticket = list(map(int, sections[1].splitlines()[1].split(",")))

    nearby_tickets = [
        list(map(int, line.split(",")))
        for line in sections[2].splitlines()[1:]
        if line.strip()
    ]

    return rules, your_ticket, nearby_tickets


def get_invalid_values(rules: dict[str, list[tuple[int, int]]], ticket: list[int]) -> list[int]:
    """Return all values on *ticket* not valid for any rule."""
    valid: set[int] = set()
    for ranges in rules.values():
        for lo, hi in ranges:
            valid.update(range(lo, hi + 1))
    return [v for v in ticket if v not in valid]


def solve(input_path: str = "advent2020/Day16/d16_input.txt") -> int:
    """Return the ticket scanning error rate (sum of invalid nearby-ticket values)."""
    text = Path(input_path).read_text()
    rules, _, nearby = parse_input(text)
    return sum(v for ticket in nearby for v in get_invalid_values(rules, ticket))


if __name__ == "__main__":
    result = solve()
    print(f"Ticket scanning error rate: {result}")
