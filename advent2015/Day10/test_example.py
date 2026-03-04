#!/usr/bin/env python3
"""Example smoke tests for Day 10."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day10 import solve as solve1
from day10_part2 import solve as solve2


def main() -> None:
    # 1 -> 11 -> 21 -> 1211 -> 111221 -> 312211 (lengths 2,2,4,6,6,6)
    from day10 import look_and_say
    assert look_and_say("1") == "11"
    assert look_and_say("11") == "21"
    assert look_and_say("21") == "1211"
    assert solve1("1\n") == 82350  # AoC: after 40 iterations from "1"
    assert solve2("1\n") == 1166642  # after 50 iterations from "1"
    print("Day 10 examples OK")


if __name__ == "__main__":
    main()
