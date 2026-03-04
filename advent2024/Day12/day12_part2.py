#!/usr/bin/env python3
"""Advent of Code 2024 Day 12 Part 2 - Garden Groups.

Price = area * number_of_sides for each region. The number of straight
fence sides equals the number of corners. Each cell contributes an outer
corner for each pair of adjacent orthogonal neighbors both outside the
region, and an inner corner when both neighbors are inside but the
diagonal between them is outside.
"""
from pathlib import Path
from collections import deque

DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))
CORNER_PAIRS = [
    ((-1, 0), (0, 1)),
    ((0, 1), (1, 0)),
    ((1, 0), (0, -1)),
    ((0, -1), (-1, 0)),
]


def solve(s: str) -> int:
    """Return total fence price (area * sides) for all regions."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    def same(r, c, ch):
        return 0 <= r < rows and 0 <= c < cols and grid[r][c] == ch

    total = 0
    for sr in range(rows):
        for sc in range(cols):
            if visited[sr][sc]:
                continue
            ch = grid[sr][sc]
            queue = deque([(sr, sc)])
            visited[sr][sc] = True
            region = []
            while queue:
                r, c = queue.popleft()
                region.append((r, c))
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if same(nr, nc, ch) and not visited[nr][nc]:
                        visited[nr][nc] = True
                        queue.append((nr, nc))

            corners = 0
            for r, c in region:
                for (dr1, dc1), (dr2, dc2) in CORNER_PAIRS:
                    n1 = same(r + dr1, c + dc1, ch)
                    n2 = same(r + dr2, c + dc2, ch)
                    if not n1 and not n2:
                        corners += 1
                    elif n1 and n2 and not same(r + dr1 + dr2, c + dc1 + dc2, ch):
                        corners += 1
            total += len(region) * corners
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d12_input.txt").read_text()))
