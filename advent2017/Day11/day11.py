#!/usr/bin/env python3
"""Advent of Code 2017 Day 11 Part 1."""

from pathlib import Path


MOV = {
    "n": (0, -1, 1),
    "ne": (1, -1, 0),
    "se": (1, 0, -1),
    "s": (0, 1, -1),
    "sw": (-1, 1, 0),
    "nw": (-1, 0, 1),
}


def dist(x: int, y: int, z: int) -> int:
    """
    Run `dist` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: x, y, z.
    - Returns the computed result for this stage of the pipeline.
    """
    return max(abs(x), abs(y), abs(z))


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    x = y = z = 0
    for t in s.strip().split(","):
        dx, dy, dz = MOV[t]
        x += dx
        y += dy
        z += dz
    return dist(x, y, z)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d11_input.txt").read_text(encoding="utf-8")))
