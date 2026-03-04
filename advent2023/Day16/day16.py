#!/usr/bin/env python3
"""Advent of Code 2023 Day 16 Part 1 - The Floor Will Be Lava.

Trace a beam of light starting top-left heading right through a grid of
mirrors (/ \\) and splitters (| -).  Count how many tiles get energized.
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
    return count_energized(grid, (0, 0, 0, 1))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d16_input.txt").read_text()))
