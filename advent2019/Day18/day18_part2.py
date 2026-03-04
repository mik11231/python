"""Advent of Code 2019 Day 18 Part 2."""

from collections import deque
from pathlib import Path
import heapq


def parse(s: str):
    """
    Run `parse` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
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
    """
    Run `neighbors` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: g, x, y.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] != '#':
            yield nx, ny


def build_graph(g, points):
    """
    Run `build_graph` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: g, points.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    out = {name: [] for name in points}
    for name, (sx, sy) in points.items():
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
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    g, (sx, sy), keys = parse(s)

    # Convert center to four-start layout.
    for dx, dy in [(0,0),(1,0),(-1,0),(0,1),(0,-1)]:
        g[sy + dy][sx + dx] = '#'
    starts = {
        '0': (sx - 1, sy - 1),
        '1': (sx + 1, sy - 1),
        '2': (sx - 1, sy + 1),
        '3': (sx + 1, sy + 1),
    }
    for p in starts.values():
        g[p[1]][p[0]] = '.'

    points = dict(starts)
    points.update(keys)
    graph = build_graph(g, points)

    all_mask = 0
    for k in keys:
        all_mask |= 1 << (ord(k) - ord('a'))

    start_state = ('0', '1', '2', '3', 0)
    pq = [(0, start_state)]
    dist = {start_state: 0}

    while pq:
        d, st = heapq.heappop(pq)
        p0, p1, p2, p3, mask = st
        if d != dist.get(st):
            continue
        if mask == all_mask:
            return d

        pos = [p0, p1, p2, p3]
        for i in range(4):
            cur = pos[i]
            for nxt, w, req in graph[cur]:
                bit = 1 << (ord(nxt) - ord('a'))
                if mask & bit:
                    continue
                if req & ~mask:
                    continue
                npos = pos.copy()
                npos[i] = nxt
                nm = mask | bit
                ns = (npos[0], npos[1], npos[2], npos[3], nm)
                nd = d + w
                if nd < dist.get(ns, 10**18):
                    dist[ns] = nd
                    heapq.heappush(pq, (nd, ns))

    raise RuntimeError('no solution')


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d18_input.txt').read_text()))
