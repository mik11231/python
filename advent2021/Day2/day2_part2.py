#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 2: Dive! (Part 2)

Commands now use an *aim* mechanic: ``down X`` / ``up X`` adjust aim,
and ``forward X`` increases horizontal by X **and** depth by aim × X.

Algorithm
---------
Single-pass interpreter tracking three values: horizontal, depth, and aim.
O(n) time.
"""

from pathlib import Path

from day2 import parse_commands


def navigate_with_aim(commands: list[tuple[str, int]]) -> tuple[int, int]:
    """Execute commands using the aim mechanic; return (horizontal, depth)."""
    horizontal = 0
    depth = 0
    aim = 0
    for direction, value in commands:
        if direction == "forward":
            horizontal += value
            depth += aim * value
        elif direction == "down":
            aim += value
        elif direction == "up":
            aim -= value
    return horizontal, depth


def solve(input_path: str = "advent2021/Day2/d2_input.txt") -> int:
    """Read navigation commands and return horizontal * depth (aim rules)."""
    commands = parse_commands(Path(input_path).read_text())
    horizontal, depth = navigate_with_aim(commands)
    return horizontal * depth


if __name__ == "__main__":
    result = solve()
    print(f"Horizontal × Depth (with aim) = {result}")
