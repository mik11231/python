#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 16: Ticket Translation (Part 2)

After discarding invalid nearby tickets, determine which field corresponds to
which ticket position and then compute the product of the six "departure"
fields on your own ticket.

Algorithm
---------
1. Keep only tickets with no invalid values (reuse Part 1's helpers).
2. For each position, compute the set of fields whose ranges are satisfied by
   every ticket's value at that position.
3. Constraint-propagation: repeatedly find a position with exactly one
   candidate field, assign it, and remove that field from all other positions.
4. Multiply the values of your ticket at positions assigned to "departure*"
   fields.
"""

import math
from pathlib import Path

from day16 import get_invalid_values, parse_input


def _value_matches_field(value: int, ranges: list[tuple[int, int]]) -> bool:
    """Return True if *value* falls within any of the valid ranges for a field."""
    return any(lo <= value <= hi for lo, hi in ranges)


def determine_field_positions(
    rules: dict[str, list[tuple[int, int]]],
    valid_tickets: list[list[int]],
) -> dict[str, int]:
    """Return a mapping of field-name -> position index."""
    n = len(rules)
    candidates: list[set[str]] = [set(rules.keys()) for _ in range(n)]

    for ticket in valid_tickets:
        for pos, value in enumerate(ticket):
            for name, ranges in rules.items():
                if not _value_matches_field(value, ranges):
                    candidates[pos].discard(name)

    assigned: dict[str, int] = {}
    while len(assigned) < n:
        for pos, names in enumerate(candidates):
            if len(names) == 1:
                name = next(iter(names))
                assigned[name] = pos
                for other in candidates:
                    other.discard(name)
                break
        else:
            raise RuntimeError("Constraint propagation stuck – no singleton found")

    return assigned


def solve(input_path: str = "advent2020/Day16/d16_input.txt") -> int:
    """Return the product of your ticket's six 'departure' fields."""
    text = Path(input_path).read_text()
    rules, your_ticket, nearby = parse_input(text)

    valid_tickets = [t for t in nearby if not get_invalid_values(rules, t)]
    mapping = determine_field_positions(rules, valid_tickets)

    return math.prod(
        your_ticket[pos]
        for name, pos in mapping.items()
        if name.startswith("departure")
    )


if __name__ == "__main__":
    result = solve()
    print(f"Product of departure fields: {result}")
