"""Advent of Code 2019 Day 12 Part 1."""

import re
from pathlib import Path


def load(s):
    return [list(map(int, re.findall(r'-?\d+', line))) for line in s.splitlines() if line.strip()]


def step(pos, vel):
    n = len(pos)
    for i in range(n):
        for j in range(i + 1, n):
            for a in range(3):
                if pos[i][a] < pos[j][a]:
                    vel[i][a] += 1; vel[j][a] -= 1
                elif pos[i][a] > pos[j][a]:
                    vel[i][a] -= 1; vel[j][a] += 1
    for i in range(n):
        for a in range(3):
            pos[i][a] += vel[i][a]


def solve(s: str, steps=1000) -> int:
    pos = load(s)
    vel = [[0, 0, 0] for _ in pos]
    for _ in range(steps):
        step(pos, vel)
    return sum(sum(abs(v) for v in p) * sum(abs(v) for v in q) for p, q in zip(pos, vel))


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d12_input.txt').read_text(), 1000))
