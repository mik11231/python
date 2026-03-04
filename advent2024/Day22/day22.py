#!/usr/bin/env python3
"""Advent of Code 2024 Day 22 Part 1 - Monkey Market.

Pseudo-random evolution: multiply by 64 then XOR+prune, floor-divide by 32
then XOR+prune, multiply by 2048 then XOR+prune (prune = mod 16777216).
Sum the 2000th secret number for each buyer.
"""
from pathlib import Path

PRUNE = 16777216


def evolve(secret):
    """
    Run `evolve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: secret.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    secret = (secret ^ (secret << 6)) % PRUNE
    secret = (secret ^ (secret >> 5)) % PRUNE
    secret = (secret ^ (secret << 11)) % PRUNE
    return secret


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    total = 0
    for line in s.strip().splitlines():
        secret = int(line)
        for _ in range(2000):
            secret = evolve(secret)
        total += secret
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d22_input.txt").read_text()))
