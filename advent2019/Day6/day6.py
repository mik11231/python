"""Advent of Code 2019 Day 6 Part 1."""

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
    children = defaultdict(list)
    indeg = defaultdict(int)
    nodes = set()
    for ln in lines:
        a, b = ln.split(')')
        children[a].append(b)
        indeg[b] += 1
        nodes.add(a)
        nodes.add(b)

    root = next(n for n in nodes if indeg[n] == 0)
    q = deque([(root, 0)])
    total = 0
    while q:
        u, d = q.popleft()
        total += d
        for v in children[u]:
            q.append((v, d + 1))
    return total


if __name__ == '__main__':
    lines = [x.strip() for x in Path(__file__).with_name('d6_input.txt').read_text().splitlines() if x.strip()]
    print(solve(lines))
