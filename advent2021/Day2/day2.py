#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 2: Dive! (Part 1)

The submarine accepts navigation commands: ``forward X``, ``down X``, and
``up X``.  Track horizontal position and depth, then return their product.

Algorithm
---------
Single-pass command interpreter.  ``forward`` increases horizontal position,
``down`` increases depth, ``up`` decreases depth.  O(n) time.
"""

from pathlib import Path


def parse_commands(text: str) -> list[tuple[str, int]]:
    """Parse navigation commands from raw text."""
    commands: list[tuple[str, int]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        direction, value = line.split()
        commands.append((direction, int(value)))
    return commands


def navigate(commands: list[tuple[str, int]]) -> tuple[int, int]:
    """Execute commands and return (horizontal, depth)."""
    horizontal = 0
    depth = 0
    for direction, value in commands:
        if direction == "forward":
            horizontal += value
        elif direction == "down":
            depth += value
        elif direction == "up":
            depth -= value
    return horizontal, depth


def solve(input_path: str = "advent2021/Day2/d2_input.txt") -> int:
    """Read navigation commands and return horizontal * depth."""
    commands = parse_commands(Path(input_path).read_text())
    horizontal, depth = navigate(commands)
    return horizontal * depth


if __name__ == "__main__":
    result = solve()
    print(f"Horizontal × Depth = {result}")
