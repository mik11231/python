"""Advent of Code 2018 solution module."""

from pathlib import Path
from day18 import load, step, value


def solve(grid: list[list[str]], target: int = 1_000_000_000) -> int:
    """Use cycle detection to skip from early state to target minute."""
    seen = {}
    minute = 0

    while minute < target:
        key = tuple(''.join(row) for row in grid)
        if key in seen:
            cycle_start = seen[key]
            cycle_len = minute - cycle_start
            remaining = target - minute
            skip = remaining // cycle_len
            if skip > 0:
                minute += skip * cycle_len
                continue
        else:
            seen[key] = minute

        grid = step(grid)
        minute += 1

    return value(grid)


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d18_input.txt'))))
