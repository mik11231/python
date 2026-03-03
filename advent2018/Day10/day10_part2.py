"""Advent of Code 2018 solution module."""

from pathlib import Path
from day10 import solve


if __name__ == "__main__":
    _, t = solve(Path(__file__).with_name("d10_input.txt"))
    print(t)
