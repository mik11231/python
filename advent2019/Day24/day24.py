"""Advent of Code 2019 Day 24 Part 1."""

from pathlib import Path


def step(g):
    h, w = 5, 5
    out = [['.' for _ in range(w)] for _ in range(h)]
    for y in range(h):
        for x in range(w):
            n = 0
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and g[ny][nx] == '#':
                    n += 1
            if g[y][x] == '#':
                out[y][x] = '#' if n == 1 else '.'
            else:
                out[y][x] = '#' if n in (1,2) else '.'
    return out


def bio(g):
    b = 0
    k = 0
    for y in range(5):
        for x in range(5):
            if g[y][x] == '#':
                b += 1 << k
            k += 1
    return b


def solve(s: str) -> int:
    g = [list(r.strip()) for r in s.splitlines() if r.strip()]
    seen = set()
    while True:
        b = bio(g)
        if b in seen:
            return b
        seen.add(b)
        g = step(g)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d24_input.txt').read_text()))
