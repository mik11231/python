"""Advent of Code 2018 solution module."""

from itertools import cycle
from pathlib import Path


def load_changes(path: Path) -> list[int]:
    """
    Run `load_changes` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    return [int(line.strip()) for line in path.read_text().splitlines() if line.strip()]


def solve(changes: list[int]) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: changes.
    - Returns the computed result for this stage of the pipeline.
    """
    seen = {0}
    frequency = 0
    for delta in cycle(changes):
        frequency += delta
        if frequency in seen:
            return frequency
        seen.add(frequency)
    raise RuntimeError("No repeated frequency found")


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d1_input.txt")
    print(solve(load_changes(input_path)))
