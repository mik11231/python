#!/usr/bin/env python3
"""Advent of Code 2017 Day 23 Part 2."""

from pathlib import Path


def is_prime(n: int) -> bool:
    """
    Run `is_prime` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: n.
    - Returns the computed result for this stage of the pipeline.
    """
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def solve(_: str) -> int:
    # Program initialization when a=1:
    # b = 65*100 + 100000 = 106500
    # c = b + 17000 = 123500
    # then count non-primes from b..c stepping by 17.
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: _.
    - Returns the computed result for this stage of the pipeline.
    """
    b = 65 * 100 + 100000
    c = b + 17000
    return sum(1 for x in range(b, c + 1, 17) if not is_prime(x))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d23_input.txt").read_text(encoding="utf-8")))
