#!/usr/bin/env python3
"""Advent of Code 2023 Day 15 Part 1 - Lens Library.

Apply the HASH algorithm to each comma-separated step: for each character,
current_value = (current_value + ord(ch)) * 17 % 256.  Sum all results.
"""
from pathlib import Path


def hash_algo(s: str) -> int:
    """
    Run `hash_algo` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    val = 0
    for ch in s:
        val = (val + ord(ch)) * 17 % 256
    return val


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    return sum(hash_algo(step) for step in s.strip().split(","))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d15_input.txt").read_text()))
