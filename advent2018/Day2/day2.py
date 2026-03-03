"""Advent of Code 2018 solution module."""

from collections import Counter
from pathlib import Path


def load_ids(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def solve(ids: list[str]) -> int:
    twos = 0
    threes = 0
    for box_id in ids:
        counts = Counter(box_id).values()
        twos += 2 in counts
        threes += 3 in counts
    return twos * threes


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d2_input.txt")
    print(solve(load_ids(input_path)))
