"""Advent of Code 2018 solution module."""

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


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


def solve(bots) -> int:
    strongest = max(bots, key=lambda b: b[3])
    sx, sy, sz, sr = strongest
    return sum(1 for x, y, z, _ in bots if abs(x - sx) + abs(y - sy) + abs(z - sz) <= sr)


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d23_input.txt'))))
