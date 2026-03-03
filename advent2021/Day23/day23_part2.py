#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 23: Amphipod (Part 2)

The side rooms are now 4 deep.  Insert two extra rows between the
existing top and bottom rows of each room:

    Row 1 (inserted): D C B A
    Row 2 (inserted): D B A C

Algorithm
---------
Reuses ``parse_input`` and ``solve_amphipod`` from Part 1.  The same
Dijkstra approach applies — the state space is larger but still tractable.
"""

from pathlib import Path

from day23 import parse_input, solve_amphipod

EXTRA_ROWS = [
    ["D", "C", "B", "A"],
    ["D", "B", "A", "C"],
]


def expand_rooms(rooms: list[list[str]]) -> list[list[str]]:
    """Insert the two extra rows between existing top and bottom rows."""
    expanded: list[list[str]] = []
    for i in range(4):
        expanded.append(
            [rooms[i][0], EXTRA_ROWS[0][i], EXTRA_ROWS[1][i], rooms[i][1]]
        )
    return expanded


def solve(input_path: str = "advent2021/Day23/d23_input.txt") -> int:
    """Return the minimum energy for the Part 2 (room-size 4) puzzle."""
    text = Path(input_path).read_text()
    rooms = parse_input(text)
    rooms = expand_rooms(rooms)
    return solve_amphipod(rooms, room_size=4)


if __name__ == "__main__":
    print(f"Minimum energy (Part 2): {solve()}")
