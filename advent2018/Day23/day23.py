"""Advent of Code 2018 solution module."""

import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.geometry import manhattan3


def load(path: Path):
    bots = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        x, y, z, r = map(int, re.findall(r'-?\d+', line))
        bots.append((x, y, z, r))
    return bots


def manhattan(a, b):
    return manhattan3(a, b)


def solve(bots) -> int:
    strongest = max(bots, key=lambda b: b[3])
    sx, sy, sz, sr = strongest
    center = (sx, sy, sz)
    return sum(1 for x, y, z, _ in bots if manhattan3((x, y, z), center) <= sr)


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d23_input.txt'))))
