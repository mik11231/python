"""Advent of Code 2019 Day 24 Part 2."""

from collections import defaultdict
from pathlib import Path


def nbrs(z, x, y):
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x + dx, y + dy
        if (nx, ny) == (2, 2):
            # into inner level
            iz = z + 1
            if x == 1 and y == 2:
                for yy in range(5):
                    yield iz, 0, yy
            elif x == 3 and y == 2:
                for yy in range(5):
                    yield iz, 4, yy
            elif x == 2 and y == 1:
                for xx in range(5):
                    yield iz, xx, 0
            elif x == 2 and y == 3:
                for xx in range(5):
                    yield iz, xx, 4
        elif nx < 0:
            yield z - 1, 1, 2
        elif nx > 4:
            yield z - 1, 3, 2
        elif ny < 0:
            yield z - 1, 2, 1
        elif ny > 4:
            yield z - 1, 2, 3
        else:
            yield z, nx, ny


def solve(s: str, minutes=200) -> int:
    bugs = set()
    g = [list(r.strip()) for r in s.splitlines() if r.strip()]
    for y in range(5):
        for x in range(5):
            if g[y][x] == '#':
                bugs.add((0, x, y))

    for _ in range(minutes):
        cnt = defaultdict(int)
        for z, x, y in bugs:
            if (x, y) == (2, 2):
                continue
            for nz, nx, ny in nbrs(z, x, y):
                if (nx, ny) != (2, 2):
                    cnt[(nz, nx, ny)] += 1

        nxt = set()
        cells = set(cnt.keys()) | bugs
        for c in cells:
            z, x, y = c
            if (x, y) == (2, 2):
                continue
            n = cnt.get(c, 0)
            if c in bugs and n == 1:
                nxt.add(c)
            if c not in bugs and n in (1, 2):
                nxt.add(c)
        bugs = nxt

    return len(bugs)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d24_input.txt').read_text(), 200))
