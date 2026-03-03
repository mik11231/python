"""Advent of Code 2019 Day 3 Part 2."""

from pathlib import Path


DIR = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def steps_map(wire: str) -> dict[tuple[int, int], int]:
    x = y = 0
    steps = 0
    out = {}
    for move in wire.split(','):
        d = move[0]
        n = int(move[1:])
        dx, dy = DIR[d]
        for _ in range(n):
            x += dx
            y += dy
            steps += 1
            out.setdefault((x, y), steps)
    return out


def solve(w1: str, w2: str) -> int:
    a = steps_map(w1)
    b = steps_map(w2)
    inter = a.keys() & b.keys()
    return min(a[p] + b[p] for p in inter)


if __name__ == '__main__':
    a, b = [line.strip() for line in Path(__file__).with_name('d3_input.txt').read_text().splitlines() if line.strip()]
    print(solve(a, b))
