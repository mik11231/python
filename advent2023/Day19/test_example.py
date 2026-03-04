#!/usr/bin/env python3
"""Tests for Day 19 using the example from the problem statement.

Part 1: sum of accepted part ratings = 19114.
Part 2: total accepted combinations = 167409079868000.
"""

from day19 import solve as solve_p1
from day19_part2 import solve as solve_p2

EXAMPLE = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


def test_part1():
    assert solve_p1(EXAMPLE) == 19114


def test_part2():
    assert solve_p2(EXAMPLE) == 167409079868000


if __name__ == "__main__":
    test_part1()
    print("PASS  Part 1: 19114")
    test_part2()
    print("PASS  Part 2: 167409079868000")
    print("\nAll Day 19 tests passed!")
