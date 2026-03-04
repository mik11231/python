#!/usr/bin/env python3
"""Example smoke tests for Day 19."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day19 import solve as solve1
from day19_part2 import solve as solve2


def main() -> None:
    inp = "H => HO\nH => OH\nO => HH\n\nHOH"
    assert solve1(inp) == 4  # HOOH, HOHO, OHOH, HHOH
    # Part 2 needs rules that include e (e => H, e => O) to reduce to e
    inp2 = "e => H\ne => O\nH => HO\nH => OH\nO => HH\n\nHOH"
    assert solve2(inp2) == 3  # HOH -> HH (OH->H) -> O (HH->O) -> e (O->e)
    print("Day 19 examples OK")


if __name__ == "__main__":
    main()
