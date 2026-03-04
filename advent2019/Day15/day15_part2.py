"""Advent of Code 2019 Day 15 Part 2."""

from collections import deque
from pathlib import Path
from day15 import DIRS, explore


def solve(program):
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    grid, oxy = explore(program)
    q = deque([(oxy, 0)])
    seen = {oxy}
    best = 0
    while q:
        (x, y), d = q.popleft()
        best = max(best, d)
        for dx, dy in DIRS.values():
            np = (x + dx, y + dy)
            if np in seen or grid.get(np, 0) == 0:
                continue
            seen.add(np)
            q.append((np, d + 1))
    return best


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d15_input.txt').read_text().strip().split(',')]
    print(solve(p))
