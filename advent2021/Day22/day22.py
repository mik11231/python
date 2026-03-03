#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 22: Reactor Reboot (Part 1)

Process cuboid on/off instructions, considering only the initialisation
region x=-50..50, y=-50..50, z=-50..50.  Count the cubes that are ON.

Algorithm
---------
The initialisation region is at most 101^3 ~ 1 M cubes, so we keep a set
of (x, y, z) tuples and process each instruction clipped to -50..50.
"""

import re
from pathlib import Path


def parse_steps(
    text: str,
) -> list[tuple[str, int, int, int, int, int, int]]:
    """Parse reboot steps into (action, x1, x2, y1, y2, z1, z2) tuples."""
    steps: list[tuple[str, int, int, int, int, int, int]] = []
    for line in text.strip().splitlines():
        action = "on" if line.startswith("on") else "off"
        nums = list(map(int, re.findall(r"-?\d+", line)))
        steps.append((action, nums[0], nums[1], nums[2], nums[3], nums[4], nums[5]))
    return steps


def solve(input_path: str = "advent2021/Day22/d22_input.txt") -> int:
    """Count ON cubes in the -50..50 initialisation region."""
    text = Path(input_path).read_text()
    steps = parse_steps(text)
    on_cubes: set[tuple[int, int, int]] = set()

    for action, x1, x2, y1, y2, z1, z2 in steps:
        cx1, cx2 = max(x1, -50), min(x2, 50)
        cy1, cy2 = max(y1, -50), min(y2, 50)
        cz1, cz2 = max(z1, -50), min(z2, 50)
        if cx1 > cx2 or cy1 > cy2 or cz1 > cz2:
            continue
        for x in range(cx1, cx2 + 1):
            for y in range(cy1, cy2 + 1):
                for z in range(cz1, cz2 + 1):
                    if action == "on":
                        on_cubes.add((x, y, z))
                    else:
                        on_cubes.discard((x, y, z))

    return len(on_cubes)


if __name__ == "__main__":
    print(f"ON cubes in initialisation region: {solve()}")
