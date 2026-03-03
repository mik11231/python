#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 11: Dumbo Octopus (Part 1)

A 10×10 grid of octopus energy levels (0-9).  Each step:

1. Increase every energy level by 1.
2. Any octopus with energy > 9 *flashes*, increasing all 8 neighbors by 1.
3. Flashing cascades; each octopus flashes at most once per step.
4. Flashed octopuses reset to 0.

Count the total number of flashes after 100 steps.

Algorithm
---------
Simulate each step with BFS-like cascade: after the global increment,
enqueue all cells > 9.  Process the queue, incrementing neighbors and
enqueuing any that newly exceed 9.  Reset flashed cells and count them.
O(steps × rows × cols) with constant-factor neighbor work.
"""

from collections import deque
from pathlib import Path


def parse_grid(text: str) -> list[list[int]]:
    """Parse the octopus energy grid from text."""
    return [
        [int(ch) for ch in line]
        for line in text.splitlines()
        if line.strip()
    ]


def step(grid: list[list[int]]) -> int:
    """Advance the grid by one step and return the number of flashes."""
    rows, cols = len(grid), len(grid[0])
    flashed: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque()

    for r in range(rows):
        for c in range(cols):
            grid[r][c] += 1
            if grid[r][c] > 9:
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        if (r, c) in flashed:
            continue
        flashed.add((r, c))
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    grid[nr][nc] += 1
                    if grid[nr][nc] > 9 and (nr, nc) not in flashed:
                        queue.append((nr, nc))

    for r, c in flashed:
        grid[r][c] = 0

    return len(flashed)


def solve(input_path: str = "advent2021/Day11/d11_input.txt") -> int:
    """Read the octopus grid and return total flashes after 100 steps."""
    text = Path(input_path).read_text()
    grid = parse_grid(text)
    return sum(step(grid) for _ in range(100))


if __name__ == "__main__":
    result = solve()
    print(f"Total flashes after 100 steps: {result}")
