"""Advent of Code 2019 Day 12 Part 2."""

import math
import re
from pathlib import Path


def load(s):
    return [list(map(int, re.findall(r'-?\d+', line))) for line in s.splitlines() if line.strip()]


def axis_period(vals):
    pos = vals[:]
    vel = [0] * len(pos)
    init = (tuple(pos), tuple(vel))
    t = 0
    while True:
        t += 1
        for i in range(len(pos)):
            for j in range(i + 1, len(pos)):
                if pos[i] < pos[j]:
                    vel[i] += 1; vel[j] -= 1
                elif pos[i] > pos[j]:
                    vel[i] -= 1; vel[j] += 1
        for i in range(len(pos)):
            pos[i] += vel[i]
        if (tuple(pos), tuple(vel)) == init:
            return t


def solve(s: str) -> int:
    pos = load(s)
    px = axis_period([p[0] for p in pos])
    py = axis_period([p[1] for p in pos])
    pz = axis_period([p[2] for p in pos])
    return math.lcm(px, py, pz)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d12_input.txt').read_text()))
