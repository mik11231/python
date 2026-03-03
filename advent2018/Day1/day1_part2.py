"""Advent of Code 2018 solution module."""

from itertools import cycle
from pathlib import Path


def load_changes(path: Path) -> list[int]:
    return [int(line.strip()) for line in path.read_text().splitlines() if line.strip()]


def solve(changes: list[int]) -> int:
    seen = {0}
    frequency = 0
    for delta in cycle(changes):
        frequency += delta
        if frequency in seen:
            return frequency
        seen.add(frequency)
    raise RuntimeError("No repeated frequency found")


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d1_input.txt")
    print(solve(load_changes(input_path)))
