#!/usr/bin/env python3
"""Example smoke tests for Day 25."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day25 import solve as solve1, index_of, code_at
from day25_part2 import solve as solve2


def main() -> None:
    # (1,1)=1, (2,1)=2, (1,2)=3, (3,1)=4, (2,2)=5, (1,3)=6
    assert index_of(1, 1) == 1
    assert index_of(2, 1) == 2
    assert index_of(1, 2) == 3
    assert index_of(3, 1) == 4
    assert index_of(2, 2) == 5
    assert index_of(1, 3) == 6
    # First code is 20151125
    assert code_at(1, 1) == 20151125
    # Second: 20151125 * 252533 mod 33554393
    assert code_at(2, 1) == 31916031
    assert code_at(1, 2) == 18749137
    text = "Enter the code at row 6, column 6."
    assert solve1(text) == 27995004  # from problem
    assert solve2("") == "Merry Christmas"
    print("Day 25 examples OK")


if __name__ == "__main__":
    main()
