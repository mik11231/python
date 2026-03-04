"""Advent of Code 2018 solution module."""

from collections import Counter
from pathlib import Path


def load_ids(path: Path) -> list[str]:
    """
    Run `load_ids` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def solve(ids: list[str]) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: ids.
    - Returns the computed result for this stage of the pipeline.
    """
    twos = 0
    threes = 0
    for box_id in ids:
        counts = Counter(box_id).values()
        twos += 2 in counts
        threes += 3 in counts
    return twos * threes


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d2_input.txt")
    print(solve(load_ids(input_path)))
