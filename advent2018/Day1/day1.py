"""Advent of Code 2018 solution module."""

from pathlib import Path


def load_changes(path: Path) -> list[int]:
    return [int(line.strip()) for line in path.read_text().splitlines() if line.strip()]


def solve(changes: list[int]) -> int:
    return sum(changes)


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d1_input.txt")
    print(solve(load_changes(input_path)))
