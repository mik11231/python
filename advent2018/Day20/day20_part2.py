"""Advent of Code 2018 solution module."""

from pathlib import Path
from day20 import build_graph, distances, load_regex


def solve(regex: str) -> int:
    d = distances(build_graph(regex))
    return sum(1 for v in d.values() if v >= 1000)


if __name__ == '__main__':
    print(solve(load_regex(Path(__file__).with_name('d20_input.txt'))))
