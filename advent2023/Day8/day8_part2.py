#!/usr/bin/env python3
"""Advent of Code 2023 Day 8 Part 2 — Haunted Wasteland.

Simultaneously navigate from every node ending in 'A' until all current nodes
end in 'Z'.  Each ghost cycles independently, so find the cycle length for each
and return their LCM.
"""
from pathlib import Path
import re
from itertools import cycle
from math import lcm


def solve(s: str) -> int:
    """Return the number of steps until all ghosts are on Z-nodes."""
    blocks = s.strip().split("\n\n")
    instructions = blocks[0].strip()
    network: dict[str, tuple[str, str]] = {}
    for line in blocks[1].splitlines():
        src, left, right = re.findall(r"[A-Z0-9]{3}", line)
        network[src] = (left, right)

    starts = [n for n in network if n.endswith("A")]
    cycle_lengths: list[int] = []
    for node in starts:
        for steps, d in enumerate(cycle(instructions), 1):
            node = network[node][0 if d == "L" else 1]
            if node.endswith("Z"):
                cycle_lengths.append(steps)
                break

    return lcm(*cycle_lengths)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d8_input.txt").read_text()))
