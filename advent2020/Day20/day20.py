#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 20: Jurassic Jigsaw (Part 1)

Reassemble a set of square image tiles into a grid so that adjacent edges
match.  Tiles may be rotated and flipped.  For Part 1 it suffices to find
the four corner tiles and return the product of their IDs.

Algorithm
---------
A corner tile is one with exactly *two* edges that don't match any other
tile.  To detect shared edges efficiently, compute a *canonical form* for
each edge: ``min(edge, reversed_edge)``.  Two tiles can be neighbours if
and only if they share a canonical edge.  Build a mapping from canonical
edge → set of tile IDs, then count, for each tile, how many of its edges
appear in more than one tile.  Tiles with exactly 2 shared edges (and thus
2 unshared / border edges) are corners.
"""

from collections import defaultdict
from math import prod
from pathlib import Path


def parse_tiles(text: str) -> dict[int, list[str]]:
    """Parse the puzzle input into ``{tile_id: [row_strings]}``."""
    tiles: dict[int, list[str]] = {}
    for block in text.strip().split("\n\n"):
        lines = block.strip().split("\n")
        tile_id = int(lines[0].split()[1].rstrip(":"))
        tiles[tile_id] = lines[1:]
    return tiles


def get_edges(grid: list[str]) -> tuple[str, str, str, str]:
    """Return ``(top, right, bottom, left)`` edge strings.

    All edges read in the natural direction for their position:
    top/bottom left-to-right, left/right top-to-bottom.
    """
    top = grid[0]
    bottom = grid[-1]
    right = "".join(row[-1] for row in grid)
    left = "".join(row[0] for row in grid)
    return top, right, bottom, left


def canonical_edge(edge: str) -> str:
    """Canonical form of an edge, invariant under horizontal flip."""
    return min(edge, edge[::-1])


def get_edge_matches(tiles: dict[int, list[str]]) -> dict[int, set[int]]:
    """Map each tile ID to the set of tile IDs that share an edge with it."""
    edge_to_tiles: dict[str, set[int]] = defaultdict(set)
    for tid, grid in tiles.items():
        for edge in get_edges(grid):
            edge_to_tiles[canonical_edge(edge)].add(tid)

    matches: dict[int, set[int]] = defaultdict(set)
    for tids in edge_to_tiles.values():
        if len(tids) == 2:
            a, b = tids
            matches[a].add(b)
            matches[b].add(a)
    return dict(matches)


def find_corners(tiles: dict[int, list[str]]) -> list[int]:
    """Return the IDs of the four corner tiles (exactly 2 shared edges)."""
    matches = get_edge_matches(tiles)
    return [tid for tid in tiles if len(matches.get(tid, set())) == 2]


def solve(input_path: str = "advent2020/Day20/d20_input.txt") -> int:
    """Read tiles, find the four corners, return the product of their IDs."""
    tiles = parse_tiles(Path(input_path).read_text())
    return prod(find_corners(tiles))


if __name__ == "__main__":
    result = solve()
    print(f"Product of the four corner tile IDs: {result}")
