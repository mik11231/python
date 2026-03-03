#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 18: Operation Order (Part 2)

Now ``+`` has **higher** precedence than ``*``.  Addition is performed before
multiplication (unless parentheses dictate otherwise).

Algorithm
---------
Reuse Part 1's ``evaluate`` with a precedence table that gives ``+`` level 2
and ``*`` level 1.
"""

from pathlib import Path

from day18 import evaluate

ADDITION_FIRST: dict[str, int] = {"+": 2, "*": 1}


def solve(input_path: str = "advent2020/Day18/d18_input.txt") -> int:
    """Sum the results of every expression with addition-first precedence."""
    lines = Path(input_path).read_text().strip().splitlines()
    return sum(evaluate(line, ADDITION_FIRST) for line in lines)


if __name__ == "__main__":
    result = solve()
    print(f"Sum of all expressions (addition-first): {result}")
