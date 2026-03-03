#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 24: Lobby Layout (Part 1)

A hex-grid floor starts all-white.  Each input line is a path of hex
directions (e, se, sw, w, nw, ne) from a reference tile.  The addressed
tile is flipped (white→black or black→white).  Count black tiles after all
flips.

Algorithm
---------
Use axial coordinates (q, r) with these direction vectors:
    e=(+1, 0)  w=(-1, 0)  se=(0, +1)  sw=(-1, +1)  ne=(+1, -1)  nw=(0, -1)
Parse each line into a sequence of moves, sum the vectors to find the target
tile, and toggle it in a set of black tiles.
"""

from pathlib import Path

HEX_DIRS: dict[str, tuple[int, int]] = {
    "e": (1, 0), "w": (-1, 0),
    "se": (0, 1), "sw": (-1, 1),
    "ne": (1, -1), "nw": (0, -1),
}


def parse_directions(line: str) -> list[str]:
    """Split a direction string into individual direction tokens."""
    dirs: list[str] = []
    i = 0
    while i < len(line):
        if line[i] in ("e", "w"):
            dirs.append(line[i])
            i += 1
        else:
            dirs.append(line[i : i + 2])
            i += 2
    return dirs


def walk(directions: list[str]) -> tuple[int, int]:
    """Follow a sequence of hex directions and return the final (q, r)."""
    q, r = 0, 0
    for d in directions:
        dq, dr = HEX_DIRS[d]
        q += dq
        r += dr
    return q, r


def identify_black_tiles(lines: list[str]) -> set[tuple[int, int]]:
    """Return the set of (q, r) coordinates that end up black."""
    black: set[tuple[int, int]] = set()
    for line in lines:
        tile = walk(parse_directions(line))
        black.symmetric_difference_update({tile})
    return black


def solve(input_path: str = "advent2020/Day24/d24_input.txt") -> int:
    """Read hex-direction lines and return the count of black tiles."""
    lines = [
        ln for ln in Path(input_path).read_text().splitlines() if ln.strip()
    ]
    return len(identify_black_tiles(lines))


if __name__ == "__main__":
    result = solve()
    print(f"Number of black tiles: {result}")
