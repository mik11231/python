#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 13: Shuttle Search (Part 1)

Given your earliest possible departure timestamp and a list of bus IDs
(where "x" means out of service), find the bus that departs soonest at or
after your timestamp.  A bus with ID *n* departs at every multiple of *n*.

Answer = bus_id * minutes_waited.

Algorithm
---------
For each bus, compute the next departure at or after the target timestamp
using ceiling division: ``next_dep = ceil(target / bus_id) * bus_id``.
Pick the bus with the smallest next departure.
"""

from pathlib import Path
from math import ceil


def parse_input(text: str) -> tuple[int, list[int]]:
    """Return (earliest_timestamp, list_of_active_bus_ids)."""
    lines = text.strip().splitlines()
    timestamp = int(lines[0])
    buses = [int(b) for b in lines[1].split(",") if b != "x"]
    return timestamp, buses


def parse_input_with_offsets(text: str) -> list[tuple[int, int]]:
    """Return list of (offset, bus_id) pairs, keeping 'x' entries out."""
    lines = text.strip().splitlines()
    entries = lines[1].split(",")
    return [(i, int(b)) for i, b in enumerate(entries) if b != "x"]


def earliest_bus(timestamp: int, buses: list[int]) -> tuple[int, int]:
    """Return (bus_id, wait_time) for the bus departing soonest."""
    best_bus, best_wait = -1, float("inf")
    for bus in buses:
        wait = (ceil(timestamp / bus) * bus) - timestamp
        if wait < best_wait:
            best_bus, best_wait = bus, wait
    return best_bus, best_wait


def solve(input_path: str = "advent2020/Day13/d13_input.txt") -> int:
    """Read bus schedule and return bus_id * wait_time."""
    text = Path(input_path).read_text()
    timestamp, buses = parse_input(text)
    bus_id, wait = earliest_bus(timestamp, buses)
    return bus_id * wait


if __name__ == "__main__":
    result = solve()
    print(f"Earliest bus ID * wait time: {result}")
