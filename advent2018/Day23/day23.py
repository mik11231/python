"""Advent of Code 2018 solution module."""

import re
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.geometry import manhattan3


def load(path: Path):
    """
    Run `load` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    bots = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        x, y, z, r = map(int, re.findall(r'-?\d+', line))
        bots.append((x, y, z, r))
    return bots


def manhattan(a, b):
    """
    Run `manhattan` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, b.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return manhattan3(a, b)


def solve(bots) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: bots.
    - Returns the computed result for this stage of the pipeline.
    """
    strongest = max(bots, key=lambda b: b[3])
    sx, sy, sz, sr = strongest
    center = (sx, sy, sz)
    return sum(1 for x, y, z, _ in bots if manhattan3((x, y, z), center) <= sr)


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d23_input.txt'))))
