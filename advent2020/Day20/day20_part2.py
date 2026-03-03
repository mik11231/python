#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 20: Jurassic Jigsaw (Part 2)

Assemble the complete image from tiles, strip each tile's 1-pixel border,
then search for *sea monsters* — a fixed 3×20 pattern of ``#`` cells.
The answer is the number of ``#`` cells that are NOT part of any sea monster.

Algorithm
---------
1. Orient a corner tile so its two unmatched edges face top and left.
2. Fill the grid left-to-right, top-to-bottom: for each cell, look up which
   un-placed tile shares the required canonical edge, then try all 8
   orientations until the exact edge match is found.
3. Strip tile borders and stitch inner pixels into one image.
4. Try all 8 orientations of the final image; the correct one contains sea
   monsters.  Subtract ``monster_count × 15`` from the total ``#`` count.
"""

import math
from collections import defaultdict
from pathlib import Path

from day20 import canonical_edge, find_corners, get_edges, parse_tiles

SEA_MONSTER_PATTERN = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]

MONSTER_COORDS: list[tuple[int, int]] = [
    (r, c)
    for r, row in enumerate(SEA_MONSTER_PATTERN)
    for c, ch in enumerate(row)
    if ch == "#"
]

MONSTER_SIZE = len(MONSTER_COORDS)  # 15


# ── Tile transformations ────────────────────────────────────────────────


def rotate(grid: list[str]) -> list[str]:
    """Rotate a grid 90° clockwise."""
    n, m = len(grid), len(grid[0])
    return ["".join(grid[n - 1 - j][i] for j in range(n)) for i in range(m)]


def flip_h(grid: list[str]) -> list[str]:
    """Mirror a grid left-to-right."""
    return [row[::-1] for row in grid]


def all_orientations(grid: list[str]):
    """Yield all 8 distinct orientations (4 rotations × 2 flips)."""
    g = list(grid)
    for _ in range(4):
        yield g
        yield flip_h(g)
        g = rotate(g)


# ── Image assembly ──────────────────────────────────────────────────────


def _build_edge_map(
    tiles: dict[int, list[str]],
) -> dict[str, set[int]]:
    """Map canonical edge string → set of tile IDs possessing that edge."""
    emap: dict[str, set[int]] = defaultdict(set)
    for tid, grid in tiles.items():
        for edge in get_edges(grid):
            emap[canonical_edge(edge)].add(tid)
    return emap


def _is_border(edge: str, emap: dict[str, set[int]]) -> bool:
    """True if *edge* belongs to only one tile (i.e. it's on the border)."""
    return len(emap[canonical_edge(edge)]) == 1


def assemble_image(
    tiles: dict[int, list[str]],
) -> list[list[tuple[int, list[str]]]]:
    """Arrange all tiles into a grid with matching edges.

    Returns a 2-D list of ``(tile_id, oriented_grid)`` tuples.
    """
    n = int(math.isqrt(len(tiles)))
    emap = _build_edge_map(tiles)

    corner_id = find_corners(tiles)[0]
    start_grid: list[str] | None = None
    for oriented in all_orientations(tiles[corner_id]):
        edges = get_edges(oriented)
        if _is_border(edges[0], emap) and _is_border(edges[3], emap):
            start_grid = oriented
            break
    assert start_grid is not None

    placed: list[list[tuple[int, list[str]] | None]] = [
        [None] * n for _ in range(n)
    ]
    placed[0][0] = (corner_id, start_grid)
    used: set[int] = {corner_id}

    for i in range(n):
        for j in range(n):
            if i == 0 and j == 0:
                continue

            req_top: str | None = None
            req_left: str | None = None
            if i > 0:
                req_top = get_edges(placed[i - 1][j][1])[2]  # type: ignore[index]
            if j > 0:
                req_left = get_edges(placed[i][j - 1][1])[1]  # type: ignore[index]

            lookup = req_top if req_top is not None else req_left
            assert lookup is not None
            candidates = emap[canonical_edge(lookup)] - used

            found = False
            for tid in candidates:
                for oriented in all_orientations(tiles[tid]):
                    edges = get_edges(oriented)
                    if (req_top is None or edges[0] == req_top) and (
                        req_left is None or edges[3] == req_left
                    ):
                        placed[i][j] = (tid, oriented)
                        used.add(tid)
                        found = True
                        break
                if found:
                    break

    return placed  # type: ignore[return-value]


def strip_borders(
    placed: list[list[tuple[int, list[str]]]],
) -> list[str]:
    """Remove the 1-pixel border from every tile and stitch into one image."""
    rows: list[str] = []
    for row_of_tiles in placed:
        tile_h = len(row_of_tiles[0][1])
        for r in range(1, tile_h - 1):
            rows.append("".join(grid[r][1:-1] for _, grid in row_of_tiles))
    return rows


# ── Sea-monster detection ───────────────────────────────────────────────


def count_sea_monsters(image: list[str]) -> int:
    """Count how many sea monsters appear in *image*."""
    h, w = len(image), len(image[0])
    mr = max(r for r, _ in MONSTER_COORDS)
    mc = max(c for _, c in MONSTER_COORDS)
    count = 0
    for r in range(h - mr):
        for c in range(w - mc):
            if all(image[r + dr][c + dc] == "#" for dr, dc in MONSTER_COORDS):
                count += 1
    return count


def solve(input_path: str = "advent2020/Day20/d20_input.txt") -> int:
    """Assemble the image, find sea monsters, return water roughness."""
    tiles = parse_tiles(Path(input_path).read_text())
    placed = assemble_image(tiles)
    image = strip_borders(placed)

    for oriented in all_orientations(image):
        monsters = count_sea_monsters(oriented)
        if monsters > 0:
            total_hash = sum(row.count("#") for row in oriented)
            return total_hash - monsters * MONSTER_SIZE

    return sum(row.count("#") for row in image)


if __name__ == "__main__":
    result = solve()
    print(f"Water roughness (# not in sea monsters): {result}")
