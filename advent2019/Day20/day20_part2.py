"""Advent of Code 2019 Day 20 Part 2."""

from collections import deque, defaultdict
from pathlib import Path


def parse(s: str):
    g = [list(r.rstrip('\n')) for r in s.splitlines()]
    h, w = len(g), max(len(r) for r in g)
    for r in g:
        if len(r) < w:
            r.extend([' '] * (w - len(r)))

    labels = defaultdict(list)
    for y in range(h):
        for x in range(w):
            if not g[y][x].isupper():
                continue
            if x + 1 < w and g[y][x + 1].isupper():
                name = g[y][x] + g[y][x + 1]
                if x - 1 >= 0 and g[y][x - 1] == '.':
                    labels[name].append((x - 1, y))
                elif x + 2 < w and g[y][x + 2] == '.':
                    labels[name].append((x + 2, y))
            if y + 1 < h and g[y + 1][x].isupper():
                name = g[y][x] + g[y + 1][x]
                if y - 1 >= 0 and g[y - 1][x] == '.':
                    labels[name].append((x, y - 1))
                elif y + 2 < h and g[y + 2][x] == '.':
                    labels[name].append((x, y + 2))

    start = labels['AA'][0]
    goal = labels['ZZ'][0]
    portal_to = {}
    outer = set()

    for k, pts in labels.items():
        if k in ('AA', 'ZZ'):
            continue
        a, b = pts
        portal_to[a] = b
        portal_to[b] = a
        for p in (a, b):
            x, y = p
            if x <= 2 or y <= 2 or x >= w - 3 or y >= h - 3:
                outer.add(p)

    return g, start, goal, portal_to, outer


def solve(s: str) -> int:
    g, start, goal, portal_to, outer = parse(s)
    q = deque([((start[0], start[1], 0), 0)])
    seen = {(start[0], start[1], 0)}

    while q:
        (x, y, z), d = q.popleft()
        if (x, y) == goal and z == 0:
            return d

        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x + dx, y + dy
            st = (nx, ny, z)
            if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] == '.' and st not in seen:
                seen.add(st)
                q.append((st, d + 1))

        if (x, y) in portal_to:
            nz = z - 1 if (x, y) in outer else z + 1
            if nz >= 0:
                nx, ny = portal_to[(x, y)]
                st = (nx, ny, nz)
                if st not in seen:
                    seen.add(st)
                    q.append((st, d + 1))

    raise RuntimeError('no path')


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d20_input.txt').read_text()))
