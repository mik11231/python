#!/usr/bin/env python3
"""Tests for Day 23 using the example from the problem statement.

Part 1: 7 triangles contain a node starting with 't'.
Part 2: largest clique is {co, de, ka, ta} -> "co,de,ka,ta".
"""

from day23 import solve as solve_p1
from day23_part2 import solve as solve_p2

EXAMPLE = """\
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 7


def test_part2():
    assert solve_p2(EXAMPLE) == "co,de,ka,ta"


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 7")
    test_part2()
    print("PASS  Part 2: co,de,ka,ta")
    print("\nAll Day 23 tests passed!")
