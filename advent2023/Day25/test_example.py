#!/usr/bin/env python3
"""Tests for Day 25 using the example from the problem statement.

Example: 15 components, cut 3 wires => groups of 9 and 6 => 54.
Part 2 is the free star.
"""

from day25 import solve as solve_p1
from day25_part2 import solve as solve_p2

EXAMPLE = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 54


def test_part2():
    assert solve_p2(EXAMPLE) == "Merry Christmas!"


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 54")
    test_part2()
    print("PASS  Part 2: Merry Christmas!")
    print("\nAll Day 25 tests passed!")
