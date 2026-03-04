"""Advent of Code 2019 Day 1 Part 2."""

from pathlib import Path


def fuel(mass: int) -> int:
    """
    Run `fuel` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: mass.
    - Returns the computed result for this stage of the pipeline.
    """
    return mass // 3 - 2


def total_fuel(mass: int) -> int:
    """
    Run `total_fuel` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: mass.
    - Returns the computed result for this stage of the pipeline.
    """
    acc = 0
    cur = fuel(mass)
    while cur > 0:
        acc += cur
        cur = fuel(cur)
    return acc


def solve(masses: list[int]) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: masses.
    - Returns the computed result for this stage of the pipeline.
    """
    return sum(total_fuel(m) for m in masses)


if __name__ == '__main__':
    masses = [int(x) for x in Path(__file__).with_name('d1_input.txt').read_text().splitlines() if x.strip()]
    print(solve(masses))
