#!/usr/bin/env python3
"""Advent of Code 2024 Day 16 Part 2 - Reindeer Maze (all best-path tiles).

Run Dijkstra forward from S and backward from E (all directions).
A tile (r,c) is on some shortest path iff there exists a direction d such that
dist_fwd[r,c,d] + dist_bwd[r,c,d] == best_score.
"""
from pathlib import Path
import heapq


def dijkstra(grid, starts):
    """Run Dijkstra from multiple (cost, r, c, d) starts. Return dist dict."""
    rows, cols = len(grid), len(grid[0])
    DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    dist = {}
    pq = list(starts)
    heapq.heapify(pq)
    while pq:
        cost, r, c, d = heapq.heappop(pq)
        if (r, c, d) in dist:
            continue
        dist[(r, c, d)] = cost
        dr, dc = DIRS[d]
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != '#':
            if (nr, nc, d) not in dist:
                heapq.heappush(pq, (cost + 1, nr, nc, d))
        for nd in [(d - 1) % 4, (d + 1) % 4]:
            if (r, c, nd) not in dist:
                heapq.heappush(pq, (cost + 1000, r, c, nd))
    return dist


def solve(s: str) -> int:
    """Return count of tiles on any shortest path from S to E."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])

    sr = sc = er = ec = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                sr, sc = r, c
            elif grid[r][c] == 'E':
                er, ec = r, c

    fwd = dijkstra(grid, [(0, sr, sc, 1)])
    # backward: start from E in all directions, but reverse the step direction
    bwd = dijkstra(grid, [(0, er, ec, d) for d in range(4)])

    best = min(fwd.get((er, ec, d), float('inf')) for d in range(4))

    tiles = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                continue
            for d in range(4):
                f = fwd.get((r, c, d), float('inf'))
                # backward direction is flipped: (d+2)%4
                b = bwd.get((r, c, (d + 2) % 4), float('inf'))
                if f + b == best:
                    tiles.add((r, c))
    return len(tiles)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d16_input.txt").read_text()))
