"""Advent of Code 2019 Day 16 Part 1."""

from pathlib import Path


BASE = [0, 1, 0, -1]


def phase(arr):
    """
    Run `phase` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: arr.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    n = len(arr)
    out = [0] * n
    for i in range(n):
        rep = i + 1
        s = 0
        for j, v in enumerate(arr):
            idx = ((j + 1) // rep) % 4
            s += v * BASE[idx]
        out[i] = abs(s) % 10
    return out


def solve(s: str) -> str:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    arr = [int(c) for c in s.strip()]
    for _ in range(100):
        arr = phase(arr)
    return ''.join(map(str, arr[:8]))


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d16_input.txt').read_text().strip()))
