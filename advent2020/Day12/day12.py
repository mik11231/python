#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 12: Rain Risk (Part 1)

The ship starts at position (0, 0) facing East.  Navigation instructions are:

  N/S/E/W <value>  — move the ship in that cardinal direction by <value> units.
  L/R <value>      — turn the ship left/right by <value> degrees.
  F <value>        — move the ship forward in its current facing by <value> units.

Return the Manhattan distance from the origin after all instructions are
processed.

Algorithm
---------
Maintain a direction index into a (dx, dy) lookup for the four cardinal
directions.  L/R rotate the index; N/S/E/W/F apply the appropriate delta
scaled by the instruction value.
"""

from pathlib import Path

DIRECTIONS = {
    0: (1, 0),    # East
    90: (0, 1),   # North
    180: (-1, 0), # West
    270: (0, -1), # South
}

MOVE = {
    "N": (0, 1),
    "S": (0, -1),
    "E": (1, 0),
    "W": (-1, 0),
}


def parse_instructions(text: str) -> list[tuple[str, int]]:
    """Parse navigation instructions from raw text."""
    return [(line[0], int(line[1:])) for line in text.splitlines() if line.strip()]


def navigate(instructions: list[tuple[str, int]]) -> tuple[int, int]:
    """Simulate the ship and return its final (x, y) position."""
    x, y = 0, 0
    facing = 0  # degrees; 0 = East, 90 = North, 180 = West, 270 = South

    for action, value in instructions:
        if action in MOVE:
            dx, dy = MOVE[action]
            x += dx * value
            y += dy * value
        elif action == "L":
            facing = (facing + value) % 360
        elif action == "R":
            facing = (facing - value) % 360
        elif action == "F":
            dx, dy = DIRECTIONS[facing]
            x += dx * value
            y += dy * value

    return x, y


def solve(input_path: str = "advent2020/Day12/d12_input.txt") -> int:
    """Read navigation instructions and return the Manhattan distance
    from the origin after following them."""
    instructions = parse_instructions(Path(input_path).read_text())
    x, y = navigate(instructions)
    return abs(x) + abs(y)


if __name__ == "__main__":
    result = solve()
    print(f"Manhattan distance from starting position: {result}")
