"""Advent of Code 2019 Day 1 Part 1."""

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
    return sum(fuel(m) for m in masses)


if __name__ == '__main__':
    masses = [int(x) for x in Path(__file__).with_name('d1_input.txt').read_text().splitlines() if x.strip()]
    print(solve(masses))
