#!/usr/bin/env python3
"""Example smoke tests for Day 4."""

from day4 import solve as solve1
from day4_part2 import solve as solve2


def main() -> None:
    assert solve1("abcdef") == 609043
    assert solve1("pqrstuv") == 1048970
    print("Day 4 examples OK")


if __name__ == "__main__":
    main()
