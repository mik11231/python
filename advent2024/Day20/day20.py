#!/usr/bin/env python3
"""Advent of Code 2024 Day 20 Part 1 - Race Condition.

BFS from S to E on a grid to get distances. A cheat passes through exactly one
wall cell (2 steps). For every pair of track cells with Manhattan distance == 2,
compute time saved = |dist[a] - dist[b]| - 2. Count cheats saving >= 100.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.runner import print_answer, read_input_for
from common import parse_track, track_distances


def solve(s: str, threshold: int = 100) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s, threshold.
    - Returns the computed result for this stage of the pipeline.
    """
    grid, start, _ = parse_track(s)
    dist = track_distances(grid, start)

    count = 0
    for (r, c), d in dist.items():
        for dr, dc in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (-1, 1), (1, -1), (1, 1)):
            nr, nc = r + dr, c + dc
            if (nr, nc) in dist:
                saved = dist[(nr, nc)] - d - 2
                if saved >= threshold:
                    count += 1
    return count


if __name__ == "__main__":
    print_answer(solve(read_input_for(__file__, "d20_input.txt")))
