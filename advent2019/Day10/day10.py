"""Advent of Code 2019 Day 10 Part 1."""

from math import gcd
from pathlib import Path


def parse(s: str):
    pts = []
    for y, row in enumerate(s.splitlines()):
        for x, ch in enumerate(row.strip()):
            if ch == '#':
                pts.append((x, y))
    return pts


def visible_from(a, pts):
    ax, ay = a
    dirs = set()
    for bx, by in pts:
        if (bx, by) == a:
            continue
        dx, dy = bx - ax, by - ay
        g = gcd(abs(dx), abs(dy))
        dirs.add((dx // g, dy // g))
    return len(dirs)


def solve(s: str) -> int:
    pts = parse(s)
    return max(visible_from(p, pts) for p in pts)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d10_input.txt').read_text()))
