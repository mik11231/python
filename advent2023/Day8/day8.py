#!/usr/bin/env python3
"""Advent of Code 2023 Day 8 Part 1 — Haunted Wasteland.

Follow L/R instructions through a node graph starting at AAA until reaching
ZZZ.  Cycle through the instruction string as needed and count steps.
"""
from pathlib import Path
import re
from itertools import cycle


def solve(s: str) -> int:
    """Return the number of steps to reach ZZZ from AAA."""
    blocks = s.strip().split("\n\n")
    instructions = blocks[0].strip()
    network: dict[str, tuple[str, str]] = {}
    for line in blocks[1].splitlines():
        src, left, right = re.findall(r"[A-Z0-9]{3}", line)
        network[src] = (left, right)

    node = "AAA"
    for steps, d in enumerate(cycle(instructions), 1):
        node = network[node][0 if d == "L" else 1]
        if node == "ZZZ":
            return steps
    return -1


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d8_input.txt").read_text()))
