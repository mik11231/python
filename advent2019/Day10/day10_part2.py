"""Advent of Code 2019 Day 10 Part 2."""

from collections import defaultdict
from math import atan2, gcd, pi
from pathlib import Path


def parse(s: str):
    """
    Run `parse` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    pts = []
    for y, row in enumerate(s.splitlines()):
        for x, ch in enumerate(row.strip()):
            if ch == '#':
                pts.append((x, y))
    return pts


def best_station(pts):
    """
    Run `best_station` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: pts.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    def vis(a):
        """
        Run `vis` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        ax, ay = a
        dirs = set()
        for bx, by in pts:
            if (bx, by) == a:
                continue
            dx, dy = bx - ax, by - ay
            g = gcd(abs(dx), abs(dy))
            dirs.add((dx // g, dy // g))
        return len(dirs)
    return max(pts, key=vis)


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    pts = parse(s)
    sx, sy = best_station(pts)

    rays = defaultdict(list)
    for x, y in pts:
        if (x, y) == (sx, sy):
            continue
        dx, dy = x - sx, y - sy
        # angle: 0 at up, increasing clockwise
        ang = (atan2(dx, -dy) + 2 * pi) % (2 * pi)
        dist = abs(dx) + abs(dy)
        rays[ang].append((dist, x, y))

    angles = sorted(rays.keys())
    for a in angles:
        rays[a].sort()

    count = 0
    while True:
        for a in angles:
            if rays[a]:
                _, x, y = rays[a].pop(0)
                count += 1
                if count == 200:
                    return 100 * x + y


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d10_input.txt').read_text()))
