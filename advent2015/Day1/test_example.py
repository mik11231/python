#!/usr/bin/env python3
"""Example smoke tests for Day 1."""

from pathlib import Path

from day1 import solve as solve1
from day1_part2 import solve as solve2


def main() -> None:
    assert solve1("(())") == 0
    assert solve1("()()") == 0
    assert solve1("(((") == 3
    assert solve1("(()(()(") == 3
    assert solve1("))(((((") == 3
    assert solve2(")") == 1
    assert solve2("()())") == 5
    print("Day 1 examples OK")


if __name__ == "__main__":
    main()
