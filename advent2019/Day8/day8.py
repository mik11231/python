"""Advent of Code 2019 Day 8 Part 1."""

from pathlib import Path


def solve(data: str, w: int = 25, h: int = 6) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: data, w, h.
    - Returns the computed result for this stage of the pipeline.
    """
    size = w * h
    layers = [data[i:i + size] for i in range(0, len(data), size)]
    best = min(layers, key=lambda x: x.count('0'))
    return best.count('1') * best.count('2')


if __name__ == '__main__':
    s = Path(__file__).with_name('d8_input.txt').read_text().strip()
    print(solve(s))
