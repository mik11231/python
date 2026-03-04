#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 9 Part 2: Movie Theater

Re-architected: validate rectangles with geometry (point-in-polygon + segment vs
rectangle interior) instead of scanning every cell. Pairs are tried by descending
area so we return the first valid one.
"""


from pathlib import Path
def _point_on_segment(px: int, py: int, ax: int, ay: int, bx: int, by: int) -> bool:
    """True if (px,py) lies on the segment from (ax,ay) to (bx,by)."""
    if (px - ax) * (by - ay) != (py - ay) * (bx - ax):
        return False
    return min(ax, bx) <= px <= max(ax, bx) and min(ay, by) <= py <= max(ay, by)


def point_in_polygon(px: int, py: int, edges: list) -> bool:
    """Ray casting: point inside closed polygon (boundary counts as inside)."""
    for (ax, ay), (bx, by) in edges:
        if _point_on_segment(px, py, ax, ay, bx, by):
            return True
    n_cross = 0
    for (ax, ay), (bx, by) in edges:
        # Horizontal edge: point on segment?
        if ay == by:
            if py == ay and min(ax, bx) <= px <= max(ax, bx):
                return True
            continue
        # Ray from (px, py) going right. Cross edge if py strictly between ay and by
        if ay < by:
            y_lo, y_hi = ay, by
        else:
            y_lo, y_hi = by, ay
        if py <= y_lo or py >= y_hi:
            continue
        # Intersection x of horizontal line y=py with edge
        t = (py - ay) / (by - ay)
        x_cross = ax + t * (bx - ax)
        if x_cross > px:
            n_cross += 1
    return n_cross % 2 == 1


def segment_intersects_rect_interior(
    sx1: int, sy1: int, sx2: int, sy2: int,
    rx1: int, ry1: int, rx2: int, ry2: int,
) -> bool:
    """True if the segment has any point strictly inside the open rectangle (rx1,ry1)-(rx2,ry2)."""
    # Endpoint inside open rect?
    if rx1 < sx1 < rx2 and ry1 < sy1 < ry2:
        return True
    if rx1 < sx2 < rx2 and ry1 < sy2 < ry2:
        return True
    # Parametric segment: (sx1,sy1) + t*((sx2-sx1),(sy2-sy1)), t in [0,1]
    dx = sx2 - sx1
    dy = sy2 - sy1
    # Check intersection with the four edges of the open rectangle
    # Bottom edge y = ry1 (open)
    if dy != 0:
        t = (ry1 - sy1) / dy
        if 0 < t < 1:
            x = sx1 + t * dx
            if rx1 < x < rx2:
                return True
    # Top edge y = ry2
    if dy != 0:
        t = (ry2 - sy1) / dy
        if 0 < t < 1:
            x = sx1 + t * dx
            if rx1 < x < rx2:
                return True
    # Left edge x = rx1
    if dx != 0:
        t = (rx1 - sx1) / dx
        if 0 < t < 1:
            y = sy1 + t * dy
            if ry1 < y < ry2:
                return True
    # Right edge x = rx2
    if dx != 0:
        t = (rx2 - sx1) / dx
        if 0 < t < 1:
            y = sy1 + t * dy
            if ry1 < y < ry2:
                return True
    return False


def rectangle_inside_polygon(rx1: int, ry1: int, rx2: int, ry2: int, edges: list) -> bool:
    """True iff the closed rectangle [rx1,ry1]-[rx2,ry2] is entirely inside the polygon."""
    # All four corners must be inside (or on boundary)
    corners = [(rx1, ry1), (rx2, ry1), (rx1, ry2), (rx2, ry2)]
    for cx, cy in corners:
        if not point_in_polygon(cx, cy, edges):
            return False
    # No polygon edge may cross the interior of the rectangle
    for (ax, ay), (bx, by) in edges:
        if segment_intersects_rect_interior(ax, ay, bx, by, rx1, ry1, rx2, ry2):
            return False
    return True


def solve():
    """Solve Day 9 Part 2: largest axis-aligned rectangle inside polygon, red corners."""
    red_tiles = []
    with open(Path(__file__).with_name('d9_input.txt'), 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                x, y = map(int, line.split(","))
                red_tiles.append((x, y))

    n = len(red_tiles)
    # Closed polygon edges: (red_tiles[i], red_tiles[(i+1) % n])
    edges = [
        (red_tiles[i], red_tiles[(i + 1) % n])
        for i in range(n)
    ]

    # All pairs with area, sorted descending (largest first)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            w = abs(x2 - x1) + 1
            h = abs(y2 - y1) + 1
            pairs.append((w * h, i, j))

    pairs.sort(key=lambda t: -t[0])

    for area, i, j in pairs:
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]
        rx1, rx2 = min(x1, x2), max(x1, x2)
        ry1, ry2 = min(y1, y2), max(y1, y2)
        if rectangle_inside_polygon(rx1, ry1, rx2, ry2, edges):
            return area

    return 0


if __name__ == "__main__":
    result = solve()
    print(f"Largest rectangle area (red+green only): {result}")
