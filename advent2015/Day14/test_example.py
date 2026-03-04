#!/usr/bin/env python3
"""Example smoke tests for Day 14."""

from day14 import solve as solve1
from day14_part2 import solve as solve2


def main() -> None:
    example = """Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds."""
    # Example from problem (race duration in puzzle is 2503)
    # Just check part 1 and 2 run and return positive int
    r1 = solve1(example)
    r2 = solve2(example)
    assert isinstance(r1, int) and r1 > 0
    assert isinstance(r2, int) and r2 > 0
    print("Part 1:", r1)
    print("Part 2:", r2)


if __name__ == "__main__":
    main()
