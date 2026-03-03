"""Advent of Code 2018 solution module."""

from pathlib import Path


def load_ids(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]


def differing_positions(left: str, right: str) -> list[int]:
    return [i for i, (lc, rc) in enumerate(zip(left, right)) if lc != rc]


def solve(ids: list[str]) -> str:
    for i, left in enumerate(ids):
        for right in ids[i + 1 :]:
            diffs = differing_positions(left, right)
            if len(diffs) == 1:
                idx = diffs[0]
                return left[:idx] + left[idx + 1 :]
    raise RuntimeError("No IDs differ by exactly one character")


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d2_input.txt")
    print(solve(load_ids(input_path)))
