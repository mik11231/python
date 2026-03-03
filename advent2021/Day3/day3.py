#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 3: Binary Diagnostic (Part 1)

Analyse the binary numbers in the diagnostic report to compute the submarine's
power consumption.  *Gamma rate*: most common bit in each position.
*Epsilon rate*: least common bit in each position.  Answer = gamma × epsilon.

Algorithm
---------
Count ones in each bit position across all numbers.  If ones ≥ half the total,
the most common bit is 1; otherwise 0.  Epsilon is the bitwise complement
(within the bit width).  O(n × b) where b is the bit width.
"""

from pathlib import Path


def most_common_bits(numbers: list[str]) -> str:
    """Return a binary string of the most common bit at each position.

    Ties (equal 0s and 1s) are broken in favour of '1'.
    """
    width = len(numbers[0])
    total = len(numbers)
    result: list[str] = []
    for col in range(width):
        ones = sum(1 for num in numbers if num[col] == "1")
        result.append("1" if ones >= (total - ones) else "0")
    return "".join(result)


def power_consumption(numbers: list[str]) -> tuple[int, int, int]:
    """Return (gamma, epsilon, gamma * epsilon)."""
    gamma_bits = most_common_bits(numbers)
    width = len(gamma_bits)
    gamma = int(gamma_bits, 2)
    epsilon = gamma ^ ((1 << width) - 1)
    return gamma, epsilon, gamma * epsilon


def solve(input_path: str = "advent2021/Day3/d3_input.txt") -> int:
    """Read the diagnostic report and return the power consumption."""
    numbers = [
        line.strip()
        for line in Path(input_path).read_text().splitlines()
        if line.strip()
    ]
    _, _, product = power_consumption(numbers)
    return product


if __name__ == "__main__":
    result = solve()
    print(f"Power consumption: {result}")
