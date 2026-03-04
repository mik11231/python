"""Advent of Code 2018 solution module."""

import re
from collections import deque
from pathlib import Path


def load_params(path: Path) -> tuple[int, int]:
    """
    Run `load_params` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    m = re.search(r"(\d+) players; last marble is worth (\d+) points", path.read_text().strip())
    return int(m.group(1)), int(m.group(2))


def play(players: int, last: int) -> int:
    """
    Run `play` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: players, last.
    - Returns the computed result for this stage of the pipeline.
    """
    circle = deque([0])
    scores = [0] * players
    for marble in range(1, last + 1):
        player = marble % players
        if marble % 23 == 0:
            circle.rotate(7)
            scores[player] += marble + circle.pop()
            circle.rotate(-1)
        else:
            circle.rotate(-1)
            circle.append(marble)
    return max(scores)


def solve(players: int, last: int) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: players, last.
    - Returns the computed result for this stage of the pipeline.
    """
    return play(players, last)


if __name__ == "__main__":
    p, l = load_params(Path(__file__).with_name("d9_input.txt"))
    print(solve(p, l))
