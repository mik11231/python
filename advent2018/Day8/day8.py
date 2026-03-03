"""Advent of Code 2018 solution module."""

from pathlib import Path


def parse_node(data: list[int], i: int = 0) -> tuple[int, int, int]:
    child_count, meta_count = data[i], data[i + 1]
    i += 2
    meta_sum = 0
    child_values = []
    for _ in range(child_count):
        i, s, v = parse_node(data, i)
        meta_sum += s
        child_values.append(v)
    metadata = data[i : i + meta_count]
    i += meta_count
    meta_sum += sum(metadata)

    if child_count == 0:
        value = sum(metadata)
    else:
        value = sum(child_values[m - 1] for m in metadata if 1 <= m <= child_count)

    return i, meta_sum, value


def load_data(path: Path) -> list[int]:
    return [int(x) for x in path.read_text().strip().split()]


def solve(data: list[int]) -> int:
    return parse_node(data)[1]


if __name__ == "__main__":
    print(solve(load_data(Path(__file__).with_name("d8_input.txt"))))
