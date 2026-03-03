#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 12: Rain Risk (Part 2)

Now there is a waypoint that starts at (10, 1) relative to the ship.
Instructions are reinterpreted:

  N/S/E/W <value>  — move the *waypoint* in that direction by <value>.
  L/R <value>      — rotate the waypoint around the ship by <value> degrees.
  F <value>        — move the ship toward the waypoint <value> times
                     (the waypoint keeps its relative position).

Return the Manhattan distance from the origin after all instructions.

Algorithm
---------
Maintain the waypoint as a relative (wx, wy) offset.  Rotation by 90 degrees
left maps (wx, wy) -> (-wy, wx).  F multiplies the offset by the value and
adds it to the ship position.
"""

from pathlib import Path

from day12 import parse_instructions

MOVE = {
    "N": (0, 1),
    "S": (0, -1),
    "E": (1, 0),
    "W": (-1, 0),
}


def rotate_waypoint(wx: int, wy: int, action: str, degrees: int) -> tuple[int, int]:
    """Rotate the waypoint around the origin by the given degrees."""
    steps = (degrees // 90) % 4
    if action == "R":
        # Convert right rotation to equivalent left rotation (e.g. R90 = L270 = 3 left steps)
        steps = (4 - steps) % 4
    for _ in range(steps):
        # Each left-90 rotation: (x, y) -> (-y, x)
        wx, wy = -wy, wx
    return wx, wy


def navigate_waypoint(instructions: list[tuple[str, int]]) -> tuple[int, int]:
    """Simulate waypoint navigation and return the ship's final position."""
    sx, sy = 0, 0
    wx, wy = 10, 1  # waypoint relative to ship

    for action, value in instructions:
        if action in MOVE:
            dx, dy = MOVE[action]
            wx += dx * value
            wy += dy * value
        elif action in ("L", "R"):
            wx, wy = rotate_waypoint(wx, wy, action, value)
        elif action == "F":
            sx += wx * value
            sy += wy * value

    return sx, sy


def solve(input_path: str = "advent2020/Day12/d12_input.txt") -> int:
    """Read navigation instructions and return the Manhattan distance
    using waypoint-based movement."""
    instructions = parse_instructions(Path(input_path).read_text())
    x, y = navigate_waypoint(instructions)
    return abs(x) + abs(y)


if __name__ == "__main__":
    result = solve()
    print(f"Manhattan distance (waypoint navigation): {result}")
