"""Advent of Code 2019 Day 20 Part 1."""

from collections import deque, defaultdict
from pathlib import Path


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
            # horizontal label
            if x + 1 < w and g[y][x + 1].isupper():
                name = g[y][x] + g[y][x + 1]
                if x - 1 >= 0 and g[y][x - 1] == '.':
                    labels[name].append((x - 1, y))
                elif x + 2 < w and g[y][x + 2] == '.':
                    labels[name].append((x + 2, y))
            # vertical label
            if y + 1 < h and g[y + 1][x].isupper():
                name = g[y][x] + g[y + 1][x]
                if y - 1 >= 0 and g[y - 1][x] == '.':
                    labels[name].append((x, y - 1))
                elif y + 2 < h and g[y + 2][x] == '.':
                    labels[name].append((x, y + 2))

    portals = {}
    for k, pts in labels.items():
        if k in ('AA', 'ZZ'):
            continue
        a, b = pts
        portals[a] = b
        portals[b] = a

    return g, labels['AA'][0], labels['ZZ'][0], portals


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
    g, start, goal, portals = parse(s)
    q = deque([(start, 0)])
    seen = {start}
    while q:
        (x, y), d = q.popleft()
        if (x, y) == goal:
            return d
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            nx, ny = x + dx, y + dy
            if 0 <= ny < len(g) and 0 <= nx < len(g[0]) and g[ny][nx] == '.' and (nx, ny) not in seen:
                seen.add((nx, ny))
                q.append(((nx, ny), d + 1))
        if (x, y) in portals and portals[(x, y)] not in seen:
            seen.add(portals[(x, y)])
            q.append((portals[(x, y)], d + 1))
    raise RuntimeError('no path')


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d20_input.txt').read_text()))
