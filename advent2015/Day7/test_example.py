#!/usr/bin/env python3
"""Example smoke tests for Day 7."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day7 import solve as solve1
from day7_part2 import solve as solve2


def main() -> None:
    ex = """123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""
    # d=72, e=507, f=492, g=114, h=65412, i=65079, x=123, y=456
    from day7 import eval_circuit, parse
    c = parse(ex)
    v = eval_circuit(c)
    assert v["d"] == 72
    assert v["e"] == 507
    assert v["f"] == 492
    assert v["g"] == 114
    assert v["h"] == 65412
    assert v["i"] == 65079
    print("Day 7 examples OK")


if __name__ == "__main__":
    main()
