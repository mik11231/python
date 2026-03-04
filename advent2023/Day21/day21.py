#!/usr/bin/env python3
"""Advent of Code 2023 Day 21 Part 1 - Step Counter.

BFS on garden grid to find how many garden plots are reachable in exactly
64 steps. A position is reachable at step N if its shortest BFS distance
shares the same parity as N.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.grid import neighbors4
from aoclib.search import bfs_distances


def solve(s: str, steps: int = 64) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s, steps.
    - Returns the computed result for this stage of the pipeline.
    """
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    sr = sc = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "S":
                sr, sc = r, c

    def _neighbors(cell: tuple[int, int]):
        """
        Run `_neighbors` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: cell.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        r, c = cell
        for nr, nc in neighbors4(r, c, rows, cols):
            if grid[nr][nc] != "#":
                yield (nr, nc)

    dist = bfs_distances((sr, sc), _neighbors)
    return sum(1 for v in dist.values() if v <= steps and v % 2 == steps % 2)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d21_input.txt").read_text()))
