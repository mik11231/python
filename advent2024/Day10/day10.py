#!/usr/bin/env python3
"""Advent of Code 2024 Day 10 Part 1 - Hoof It.

For each trailhead (height 0), BFS to find how many distinct height-9
positions are reachable via paths that increase by exactly 1 at each step.
Sum all trailhead scores.
"""
from pathlib import Path
from collections import deque


def solve(s: str) -> int:
    """Return the sum of scores of all trailheads."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    heights = [[int(ch) for ch in row] for row in grid]

    total = 0
    for sr in range(rows):
        for sc in range(cols):
            if heights[sr][sc] != 0:
                continue
            visited = {(sr, sc)}
            queue = deque([(sr, sc)])
            nines = set()
            while queue:
                r, c = queue.popleft()
                if heights[r][c] == 9:
                    nines.add((r, c))
                    continue
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < rows and 0 <= nc < cols
                            and (nr, nc) not in visited
                            and heights[nr][nc] == heights[r][c] + 1):
                        visited.add((nr, nc))
                        queue.append((nr, nc))
            total += len(nines)
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d10_input.txt").read_text()))
