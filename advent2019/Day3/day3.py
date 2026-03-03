"""Advent of Code 2019 Day 3 Part 1."""

from pathlib import Path


DIR = {'U': (0, 1), 'D': (0, -1), 'L': (-1, 0), 'R': (1, 0)}


def trace(wire: str) -> set[tuple[int, int]]:
    x = y = 0
    seen = set()
    for move in wire.split(','):
        d = move[0]
        n = int(move[1:])
        dx, dy = DIR[d]
        for _ in range(n):
            x += dx
            y += dy
            seen.add((x, y))
    return seen


def solve(w1: str, w2: str) -> int:
    inter = trace(w1) & trace(w2)
    return min(abs(x) + abs(y) for x, y in inter)


if __name__ == '__main__':
    a, b = [line.strip() for line in Path(__file__).with_name('d3_input.txt').read_text().splitlines() if line.strip()]
    print(solve(a, b))
