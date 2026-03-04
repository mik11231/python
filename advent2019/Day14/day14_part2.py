"""Advent of Code 2019 Day 14 Part 2."""

from pathlib import Path
from day14 import ore_for_fuel, parse


def solve(s: str, ore=1_000_000_000_000) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s, ore.
    - Returns the computed result for this stage of the pipeline.
    """
    rec = parse(s)
    lo, hi = 1, 1
    while ore_for_fuel(rec, hi) <= ore:
        hi *= 2
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ore_for_fuel(rec, mid) <= ore:
            lo = mid
        else:
            hi = mid - 1
    return lo


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d14_input.txt').read_text()))
