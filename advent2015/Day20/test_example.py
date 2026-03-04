#!/usr/bin/env python3
"""Example smoke tests for Day 20."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day20 import solve as solve1
from day20_part2 import solve as solve2


def main() -> None:
    # House 1: 10*1 = 10; house 2: 10*(1+2)=30; house 3: 10*(1+3)=40; ...
    # First house with >= 10 is 1; with >= 30 is 2; with >= 150 is 8 (10*(1+2+4+8)=150)
    assert solve1("10\n") == 1
    assert solve1("30\n") == 2
    assert solve1("150\n") == 8
    print("Day 20 examples OK")


if __name__ == "__main__":
    main()
