#!/usr/bin/env python3
"""Example smoke tests for Day 5."""

from day5 import solve as solve1
from day5_part2 import solve as solve2


def main() -> None:
    assert solve1("ugknbfddgicrmopn\n") == 1
    assert solve1("aaa\n") == 1
    assert solve1("jchzalrnumimnmhp\n") == 0
    assert solve1("haegwjzuvuyypxyu\n") == 0
    assert solve1("dvszwmarrgswjxmb\n") == 0
    assert solve2("qjhvhtzxzqqjkmpb\n") == 1
    assert solve2("xxyxx\n") == 1
    assert solve2("uurcxstgmygtbstg\n") == 0
    assert solve2("ieodomkazucvgmuy\n") == 0
    print("Day 5 examples OK")


if __name__ == "__main__":
    main()
