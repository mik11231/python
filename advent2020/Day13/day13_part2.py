#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 13: Shuttle Search (Part 2)

Find the earliest timestamp *t* such that bus at index *i* departs at time
``t + i`` for every active bus.  Entries marked "x" are ignored.

Algorithm
---------
This is a system of modular congruences:

    t ≡ -offset (mod bus_id)   for each (offset, bus_id)

We solve it iteratively (a special case of the Chinese Remainder Theorem for
pairwise-coprime moduli, which the puzzle input guarantees).  Starting from
the first constraint, we combine one constraint at a time: once a solution
satisfies the first *k* constraints, the combined period is the LCM of those
moduli (here simply their product, since they are coprime).  We then step by
that period until the next constraint is also satisfied.
"""

from pathlib import Path

from day13 import parse_input_with_offsets


def find_earliest_timestamp(buses: list[tuple[int, int]]) -> int:
    """Iterative CRT: return the smallest t satisfying all constraints."""
    t, step = 0, 1
    for offset, bus_id in buses:
        # Advance by the current combined period until this constraint is met
        while (t + offset) % bus_id != 0:
            t += step
        # Merge this bus into the combined period (coprime -> LCM = product)
        step *= bus_id
    return t


def solve(input_path: str = "advent2020/Day13/d13_input.txt") -> int:
    """Read bus schedule and return the earliest aligned timestamp."""
    text = Path(input_path).read_text()
    buses = parse_input_with_offsets(text)
    return find_earliest_timestamp(buses)


if __name__ == "__main__":
    result = solve()
    print(f"Earliest timestamp with sequential departures: {result}")
