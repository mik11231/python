#!/usr/bin/env python3
"""Advent of Code 2024 Day 12 Part 1 - Garden Groups.

Flood-fill to find connected regions of identical plants. For each region,
price = area * perimeter (edges touching a different region or the boundary).
"""
from pathlib import Path
from collections import deque


def solve(s: str) -> int:
    """Return total fence price (area * perimeter) for all regions."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    total = 0
    for sr in range(rows):
        for sc in range(cols):
            if visited[sr][sc]:
                continue
            ch = grid[sr][sc]
            queue = deque([(sr, sc)])
            visited[sr][sc] = True
            area = 0
            perimeter = 0
            while queue:
                r, c = queue.popleft()
                area += 1
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == ch:
                        if not visited[nr][nc]:
                            visited[nr][nc] = True
                            queue.append((nr, nc))
                    else:
                        perimeter += 1
            total += area * perimeter
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d12_input.txt").read_text()))
