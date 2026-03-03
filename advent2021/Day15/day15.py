#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 15: Chiton (Part 1)

Find the path from the top-left to the bottom-right of a risk-level grid
that minimises the total risk (the sum of risk values of every cell entered,
excluding the starting cell).

Algorithm
---------
Dijkstra's shortest-path algorithm on a 2-D grid with non-negative edge
weights.  Each cell is a node; edges connect it to its four cardinal
neighbours with weight equal to the destination cell's risk level.  A
min-heap (priority queue) always expands the lowest-cost frontier node.
"""

import heapq
from pathlib import Path


def parse_grid(text: str) -> list[list[int]]:
    """Parse a grid of single-digit risk levels from *text*."""
    return [[int(ch) for ch in line] for line in text.strip().splitlines()]


def dijkstra(grid: list[list[int]]) -> int:
    """Return the minimum total risk from top-left to bottom-right of *grid*."""
    rows, cols = len(grid), len(grid[0])
    dist = [[float("inf")] * cols for _ in range(rows)]
    dist[0][0] = 0
    heap: list[tuple[int, int, int]] = [(0, 0, 0)]

    while heap:
        cost, r, c = heapq.heappop(heap)
        if r == rows - 1 and c == cols - 1:
            return cost
        if cost > dist[r][c]:
            continue
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_cost = cost + grid[nr][nc]
                if new_cost < dist[nr][nc]:
                    dist[nr][nc] = new_cost
                    heapq.heappush(heap, (new_cost, nr, nc))

    return int(dist[rows - 1][cols - 1])


def solve(input_path: str = "advent2021/Day15/d15_input.txt") -> int:
    """Read puzzle input and return the lowest total risk path cost."""
    grid = parse_grid(Path(input_path).read_text())
    return dijkstra(grid)


if __name__ == "__main__":
    result = solve()
    print(f"Lowest total risk: {result}")
