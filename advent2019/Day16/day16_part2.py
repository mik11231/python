"""Advent of Code 2019 Day 16 Part 2."""

from pathlib import Path


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
    base = [int(c) for c in s.strip()]
    offset = int(s[:7])
    arr = (base * 10000)[offset:]

    # Offset is in second half, so each value depends only on suffix.
    for _ in range(100):
        acc = 0
        for i in range(len(arr) - 1, -1, -1):
            acc = (acc + arr[i]) % 10
            arr[i] = acc
    return ''.join(map(str, arr[:8]))


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d16_input.txt').read_text().strip()))
