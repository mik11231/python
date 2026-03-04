#!/usr/bin/env python3
"""Advent of Code 2023 Day 24 Part 1 - Never Tell Me The Odds.

For each pair of hailstones, find where their 2D (X, Y) paths intersect.
Count pairs that intersect within the test area and in the future for both.
"""
from pathlib import Path
from itertools import combinations


def solve(s: str, lo=200000000000000, hi=400000000000000) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s, lo, hi.
    - Returns the computed result for this stage of the pipeline.
    """
    stones = []
    for line in s.strip().splitlines():
        pos, vel = line.split("@")
        px, py, pz = map(int, pos.split(","))
        vx, vy, vz = map(int, vel.split(","))
        stones.append((px, py, pz, vx, vy, vz))

    count = 0
    for i, j in combinations(range(len(stones)), 2):
        px1, py1, _, vx1, vy1, _ = stones[i]
        px2, py2, _, vx2, vy2, _ = stones[j]

        det = vx1 * vy2 - vy1 * vx2
        if det == 0:
            continue

        t = ((px2 - px1) * vy2 - (py2 - py1) * vx2) / det
        u = ((px2 - px1) * vy1 - (py2 - py1) * vx1) / det

        if t < 0 or u < 0:
            continue

        ix = px1 + vx1 * t
        iy = py1 + vy1 * t

        if lo <= ix <= hi and lo <= iy <= hi:
            count += 1

    return count


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d24_input.txt").read_text()))
