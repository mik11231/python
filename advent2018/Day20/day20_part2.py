"""Advent of Code 2018 solution module."""

from pathlib import Path
from day20 import build_graph, distances, load_regex


def solve(regex: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: regex.
    - Returns the computed result for this stage of the pipeline.
    """
    d = distances(build_graph(regex))
    return sum(1 for v in d.values() if v >= 1000)


if __name__ == '__main__':
    print(solve(load_regex(Path(__file__).with_name('d20_input.txt'))))
