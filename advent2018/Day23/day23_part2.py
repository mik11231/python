"""Advent of Code 2018 solution module."""

import heapq
import re
from pathlib import Path


def load(path: Path):
    bots = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        x, y, z, r = map(int, re.findall(r'-?\d+', line))
        bots.append((x, y, z, r))
    return bots


def dist_point_to_cube(px, py, pz, x, y, z, size):
    """Manhattan distance from point to axis-aligned cube [x,x+size-1] etc."""
    dx = 0 if x <= px <= x + size - 1 else (x - px if px < x else px - (x + size - 1))
    dy = 0 if y <= py <= y + size - 1 else (y - py if py < y else py - (y + size - 1))
    dz = 0 if z <= pz <= z + size - 1 else (z - pz if pz < z else pz - (z + size - 1))
    return dx + dy + dz


def bots_in_cube(bots, x, y, z, size):
    """Upper-bound count: bots whose range intersects this cube."""
    c = 0
    for bx, by, bz, br in bots:
        if dist_point_to_cube(bx, by, bz, x, y, z, size) <= br:
            c += 1
    return c


def min_dist_cube_to_origin(x, y, z, size):
    return dist_point_to_cube(0, 0, 0, x, y, z, size)


def solve(bots):
    # Bounding cube that covers all bot centers.
    min_x = min(b[0] for b in bots)
    max_x = max(b[0] for b in bots)
    min_y = min(b[1] for b in bots)
    max_y = max(b[1] for b in bots)
    min_z = min(b[2] for b in bots)
    max_z = max(b[2] for b in bots)

    size = 1
    span = max(max_x - min_x + 1, max_y - min_y + 1, max_z - min_z + 1)
    while size < span:
        size *= 2

    # Max-heap by bot count, then min distance to origin, then smaller cube size.
    pq = []
    count = bots_in_cube(bots, min_x, min_y, min_z, size)
    heapq.heappush(pq, (-count, min_dist_cube_to_origin(min_x, min_y, min_z, size), size, min_x, min_y, min_z))

    while pq:
        neg_count, dist0, csize, x, y, z = heapq.heappop(pq)
        count = -neg_count

        if csize == 1:
            # Single point cube: optimal by heap ordering.
            return dist0

        half = csize // 2
        for dx in (0, half):
            for dy in (0, half):
                for dz in (0, half):
                    nx, ny, nz = x + dx, y + dy, z + dz
                    ncount = bots_in_cube(bots, nx, ny, nz, half)
                    ndist = min_dist_cube_to_origin(nx, ny, nz, half)
                    heapq.heappush(pq, (-ncount, ndist, half, nx, ny, nz))

    raise RuntimeError('search failed')


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d23_input.txt'))))
