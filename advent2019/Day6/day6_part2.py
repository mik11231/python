"""Advent of Code 2019 Day 6 Part 2."""

from collections import defaultdict, deque
from pathlib import Path


def solve(lines: list[str]) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: lines.
    - Returns the computed result for this stage of the pipeline.
    """
    g = defaultdict(list)
    parent = {}
    for ln in lines:
        a, b = ln.split(')')
        g[a].append(b)
        g[b].append(a)
        parent[b] = a

    src = parent['YOU']
    dst = parent['SAN']
    q = deque([(src, 0)])
    seen = {src}
    while q:
        u, d = q.popleft()
        if u == dst:
            return d
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                q.append((v, d + 1))
    raise RuntimeError('no path')


if __name__ == '__main__':
    lines = [x.strip() for x in Path(__file__).with_name('d6_input.txt').read_text().splitlines() if x.strip()]
    print(solve(lines))
