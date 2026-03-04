#!/usr/bin/env python3
"""Advent of Code 2024 Day 16 Part 1 - Reindeer Maze.

Shortest path through a maze where moving forward costs 1 and
rotating 90 degrees costs 1000. Start at S facing East, reach E.
Uses Dijkstra on state (row, col, direction).
"""
from pathlib import Path
import heapq


def solve(s: str) -> int:
    """Return the lowest possible score from S to E."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # N, E, S, W

    sr = sc = er = ec = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                sr, sc = r, c
            elif grid[r][c] == 'E':
                er, ec = r, c

    dist = {}
    start = (0, sr, sc, 1)  # cost, row, col, direction (1=East)
    pq = [start]
    while pq:
        cost, r, c, d = heapq.heappop(pq)
        if (r, c, d) in dist:
            continue
        dist[(r, c, d)] = cost
        if r == er and c == ec:
            return cost
        # move forward
        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            if (nr, nc, d) not in dist:
                heapq.heappush(pq, (cost + 1, nr, nc, d))
        # turn left / right
        for nd in [(d - 1) % 4, (d + 1) % 4]:
            if (r, c, nd) not in dist:
                heapq.heappush(pq, (cost + 1000, r, c, nd))

    return -1


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d16_input.txt").read_text()))
