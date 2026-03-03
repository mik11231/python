#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 2: Password Philosophy (Part 1)

Each line of the input describes a policy and a password:
    <min>-<max> <letter>: <password>

A password is valid when <letter> appears at least <min> and at most <max>
times in <password>.

The answer is the number of valid passwords in the list.
"""

from pathlib import Path


def parse_line(line: str) -> tuple[int, int, str, str]:
    """Parse a policy line into (min_count, max_count, letter, password)."""
    policy, password = line.split(": ")
    counts, letter = policy.split(" ")
    lo, hi = counts.split("-")
    return int(lo), int(hi), letter, password


def is_valid_sled_policy(min_count: int, max_count: int, letter: str, password: str) -> bool:
    """Return True if *letter* appears between *min_count* and *max_count*
    times (inclusive) in *password*."""
    return min_count <= password.count(letter) <= max_count


def solve(input_path: str = "advent2020/Day2/d2_input.txt") -> int:
    """Count how many passwords satisfy the sled-rental-shop policy."""
    lines = Path(input_path).read_text().splitlines()
    return sum(1 for line in lines if line.strip() and is_valid_sled_policy(*parse_line(line)))


if __name__ == "__main__":
    result = solve()
    print(f"Valid passwords (sled policy): {result}")
