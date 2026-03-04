#!/usr/bin/env python3
"""Day 12 example test from the puzzle description."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Day12.day12 import all_variants, can_fit_exact, parse_input


EXAMPLE = """0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


def parse_example() -> tuple[list[set[tuple[int, int]]], list[tuple[int, int, list[int]]]]:
    tmp = Path("Day12") / "_tmp_example_input.txt"
    tmp.write_text(EXAMPLE, encoding="utf-8")
    try:
        return parse_input(tmp)
    finally:
        tmp.unlink(missing_ok=True)


def main() -> None:
    shapes, regions = parse_example()
    variants = [all_variants(s) for s in shapes]
    areas = [len(s) for s in shapes]

    got = 0
    for w, h, counts in regions:
        if can_fit_exact(w, h, counts, variants, areas):
            got += 1

    expected = 2
    print(f"Day 12 example fitting regions: {got} (expected {expected})")
    if got != expected:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
