#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 22: Reactor Reboot (Part 2)

Full-range reactor reboot with no clipping.  Coordinates can be huge, so
the brute-force set approach from Part 1 is infeasible.

Algorithm
---------
Maintain a list of *signed* cuboids (volume, +1 or -1).  For each new
instruction, compute its intersection with every existing cuboid and add
the intersection with the **opposite** sign (inclusion-exclusion to cancel
double-counting).  If the instruction is "on", also add the new cuboid
with sign +1.  The total ON count is the sum of (sign * volume) over all
stored cuboids.
"""

from pathlib import Path

from day22 import parse_steps


def _intersect(
    a: tuple[int, ...], b: tuple[int, ...]
) -> tuple[int, int, int, int, int, int] | None:
    """Return the intersection cuboid (x1,x2,y1,y2,z1,z2) or None."""
    x1 = max(a[0], b[0])
    x2 = min(a[1], b[1])
    y1 = max(a[2], b[2])
    y2 = min(a[3], b[3])
    z1 = max(a[4], b[4])
    z2 = min(a[5], b[5])
    if x1 <= x2 and y1 <= y2 and z1 <= z2:
        return (x1, x2, y1, y2, z1, z2)
    return None


def count_on_cubes(
    steps: list[tuple[str, int, int, int, int, int, int]],
) -> int:
    """Return the total number of ON cubes after processing all steps."""
    cuboids: list[tuple[int, int, int, int, int, int, int]] = []

    for action, x1, x2, y1, y2, z1, z2 in steps:
        new_cuboid = (x1, x2, y1, y2, z1, z2)
        additions: list[tuple[int, int, int, int, int, int, int]] = []

        for *coords, sign in cuboids:
            overlap = _intersect(tuple(coords), new_cuboid)
            if overlap is not None:
                additions.append((*overlap, -sign))

        if action == "on":
            additions.append((*new_cuboid, 1))

        cuboids.extend(additions)

    total = 0
    for x1, x2, y1, y2, z1, z2, sign in cuboids:
        total += sign * (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
    return total


def solve(input_path: str = "advent2021/Day22/d22_input.txt") -> int:
    """Count all ON cubes after the full reboot sequence."""
    text = Path(input_path).read_text()
    steps = parse_steps(text)
    return count_on_cubes(steps)


if __name__ == "__main__":
    print(f"Total ON cubes: {solve()}")
