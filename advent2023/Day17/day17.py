#!/usr/bin/env python3
"""Advent of Code 2023 Day 17 Part 1 - Clumsy Crucible.

Find the minimum heat-loss path from top-left to bottom-right using Dijkstra.
The crucible cannot move more than 3 blocks in a straight line and cannot
reverse.  State = (row, col, direction, consecutive_steps).
"""
from pathlib import Path
import heapq


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # (cost, row, col, dir_index, consecutive)
    pq: list[tuple[int, int, int, int, int]] = []
    heapq.heappush(pq, (0, 0, 0, -1, 0))
    visited: set[tuple[int, int, int, int]] = set()

    while pq:
        cost, r, c, d, consec = heapq.heappop(pq)
        if r == rows - 1 and c == cols - 1:
            return cost

        if (r, c, d, consec) in visited:
            continue
        visited.add((r, c, d, consec))

        for nd in range(4):
            if d != -1 and (nd + 2) % 4 == d:
                continue
            nc = consec + 1 if nd == d else 1
            if nc > 3:
                continue
            nr, ncc = r + dirs[nd][0], c + dirs[nd][1]
            if 0 <= nr < rows and 0 <= ncc < cols:
                new_cost = cost + int(grid[nr][ncc])
                if (nr, ncc, nd, nc) not in visited:
                    heapq.heappush(pq, (new_cost, nr, ncc, nd, nc))

    return -1


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d17_input.txt").read_text()))
