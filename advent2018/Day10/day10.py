"""Advent of Code 2018 solution module."""

import re
from pathlib import Path

LINE_RE = re.compile(r"position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>")


def load(path: Path):
    pts = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        x, y, vx, vy = map(int, LINE_RE.match(line).groups())
        pts.append((x, y, vx, vy))
    return pts


def at_time(pts, t):
    return [(x + vx * t, y + vy * t) for x, y, vx, vy in pts]


def bbox_area(pos):
    xs = [x for x, _ in pos]
    ys = [y for _, y in pos]
    return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1)


def find_best_time(pts):
    t = 0
    prev = bbox_area(at_time(pts, 0))
    while True:
        t += 1
        cur = bbox_area(at_time(pts, t))
        if cur > prev:
            return t - 1
        prev = cur


def render(pos):
    xs = [x for x, _ in pos]
    ys = [y for _, y in pos]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    s = set(pos)
    rows = []
    for y in range(min_y, max_y + 1):
        rows.append("".join("#" if (x, y) in s else "." for x in range(min_x, max_x + 1)))
    return "\n".join(rows)


def solve(path: Path):
    pts = load(path)
    t = find_best_time(pts)
    msg = render(at_time(pts, t))
    return msg, t


if __name__ == "__main__":
    message, _ = solve(Path(__file__).with_name("d10_input.txt"))
    print(message)
