#!/usr/bin/env python3
"""Advent of Code 2023 Day 16 Part 2 - The Floor Will Be Lava.

Try every possible starting edge tile and direction, returning the
maximum number of energized tiles from any single starting configuration.
"""
from pathlib import Path
from collections import deque


def count_energized(grid: list[str], start: tuple[int, int, int, int]) -> int:
    """
    Run `count_energized` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid, start.
    - Returns the computed result for this stage of the pipeline.
    """
    rows, cols = len(grid), len(grid[0])
    seen: set[tuple[int, int, int, int]] = set()
    q: deque[tuple[int, int, int, int]] = deque([start])

    while q:
        r, c, dr, dc = q.popleft()
        if not (0 <= r < rows and 0 <= c < cols):
            continue
        if (r, c, dr, dc) in seen:
            continue
        seen.add((r, c, dr, dc))

        ch = grid[r][c]
        if ch == ".":
            q.append((r + dr, c + dc, dr, dc))
        elif ch == "/":
            ndr, ndc = -dc, -dr
            q.append((r + ndr, c + ndc, ndr, ndc))
        elif ch == "\\":
            ndr, ndc = dc, dr
            q.append((r + ndr, c + ndc, ndr, ndc))
        elif ch == "|":
            if dc == 0:
                q.append((r + dr, c + dc, dr, dc))
            else:
                q.append((r - 1, c, -1, 0))
                q.append((r + 1, c, 1, 0))
        elif ch == "-":
            if dr == 0:
                q.append((r + dr, c + dc, dr, dc))
            else:
                q.append((r, c - 1, 0, -1))
                q.append((r, c + 1, 0, 1))

    return len({(r, c) for r, c, _, _ in seen})


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    best = 0

    for r in range(rows):
        best = max(best, count_energized(grid, (r, 0, 0, 1)))
        best = max(best, count_energized(grid, (r, cols - 1, 0, -1)))
    for c in range(cols):
        best = max(best, count_energized(grid, (0, c, 1, 0)))
        best = max(best, count_energized(grid, (rows - 1, c, -1, 0)))

    return best


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d16_input.txt").read_text()))
