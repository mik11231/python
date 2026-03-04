"""Advent of Code 2019 Day 11 Part 2."""

from pathlib import Path
from day11 import paint


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
    grid, _ = paint(program, 1)
    xs = [x for x, y in grid if grid[(x, y)] == 1]
    ys = [y for x, y in grid if grid[(x, y)] == 1]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    rows = []
    for y in range(miny, maxy + 1):
        rows.append(''.join('##' if grid.get((x, y), 0) == 1 else '  ' for x in range(minx, maxx + 1)))
    return '\n'.join(rows)


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d11_input.txt').read_text().strip().split(',')]
    print(solve(p))
