"""Advent of Code 2018 solution module."""

from pathlib import Path
from day17 import load_clay, simulate


def solve(path: Path) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    clay, min_y, max_y = load_clay(path)
    _, settled = simulate(clay, min_y, max_y)
    return sum(1 for _, y in settled if min_y <= y <= max_y)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d17_input.txt')))
