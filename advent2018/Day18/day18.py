"""Advent of Code 2018 solution module."""

from collections import Counter
from pathlib import Path


def load(path: Path) -> list[list[str]]:
    """
    Run `load` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    return [list(line.strip()) for line in path.read_text().splitlines() if line.strip()]


def step(grid: list[list[str]]) -> list[list[str]]:
    """Apply one minute of area transformation rules."""
    h, w = len(grid), len(grid[0])
    out = [row[:] for row in grid]

    for y in range(h):
        for x in range(w):
            neigh = []
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        neigh.append(grid[ny][nx])
            c = Counter(neigh)

            if grid[y][x] == '.':
                out[y][x] = '|' if c['|'] >= 3 else '.'
            elif grid[y][x] == '|':
                out[y][x] = '#' if c['#'] >= 3 else '|'
            else:
                out[y][x] = '#' if (c['#'] >= 1 and c['|'] >= 1) else '.'

    return out


def value(grid: list[list[str]]) -> int:
    """
    Run `value` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid.
    - Returns the computed result for this stage of the pipeline.
    """
    flat = [c for row in grid for c in row]
    return flat.count('|') * flat.count('#')


def solve(grid: list[list[str]]) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid.
    - Returns the computed result for this stage of the pipeline.
    """
    for _ in range(10):
        grid = step(grid)
    return value(grid)


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d18_input.txt'))))
