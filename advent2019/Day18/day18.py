"""Advent of Code 2019 Day 18 Part 1."""

from collections import deque
from functools import lru_cache
from pathlib import Path
import heapq


def parse(s: str):
    g = [list(r) for r in s.splitlines() if r]
    h, w = len(g), len(g[0])
    start = None
    keys = {}
    for y in range(h):
        for x in range(w):
            c = g[y][x]
            if c == '@':
                start = (x, y)
            elif 'a' <= c <= 'z':
                keys[c] = (x, y)
    return g, start, keys


def neighbors(g, x, y):
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] != '#':
            yield nx, ny


def build_graph(g, points):
    """For each point-of-interest, list reachable keys with distance and required doors."""
    out = {name: [] for name in points}
    pos_by_name = {name: p for name, p in points.items()}

    for name, (sx, sy) in pos_by_name.items():
        q = deque([(sx, sy, 0, 0)])
        seen = {(sx, sy)}
        while q:
            x, y, d, req = q.popleft()
            c = g[y][x]
            nreq = req
            if 'A' <= c <= 'Z':
                nreq |= 1 << (ord(c.lower()) - ord('a'))
            if 'a' <= c <= 'z' and c != name:
                out[name].append((c, d, nreq))
            for nx, ny in neighbors(g, x, y):
                if (nx, ny) not in seen:
                    seen.add((nx, ny))
                    q.append((nx, ny, d + 1, nreq))
    return out


def solve(s: str) -> int:
    g, start, keys = parse(s)
    points = {'@': start} | keys
    graph = build_graph(g, points)

    all_mask = 0
    for k in keys:
        all_mask |= 1 << (ord(k) - ord('a'))

    pq = [(0, '@', 0)]
    dist = {('@', 0): 0}

    while pq:
        d, cur, mask = heapq.heappop(pq)
        if d != dist.get((cur, mask)):
            continue
        if mask == all_mask:
            return d

        for nxt, w, req in graph[cur]:
            bit = 1 << (ord(nxt) - ord('a'))
            if mask & bit:
                continue
            if req & ~mask:
                continue
            nm = mask | bit
            nd = d + w
            st = (nxt, nm)
            if nd < dist.get(st, 10**18):
                dist[st] = nd
                heapq.heappush(pq, (nd, nxt, nm))

    raise RuntimeError('no solution')


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d18_input.txt').read_text()))
