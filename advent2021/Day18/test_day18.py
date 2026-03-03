#!/usr/bin/env python3
"""Tests for Day 18: Snailfish."""

import copy
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day18 import parse_snailfish, add, magnitude

EXAMPLE = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""


def test_part1_example():
    """Magnitude of the final sum of the example list is 4140."""
    lines = EXAMPLE.strip().splitlines()
    numbers = [parse_snailfish(line) for line in lines]
    result = numbers[0]
    for num in numbers[1:]:
        result = add(result, num)
    assert magnitude(result) == 4140


def test_part2_example():
    """Largest magnitude from any two-number sum in the example is 3993."""
    lines = EXAMPLE.strip().splitlines()
    numbers = [parse_snailfish(line) for line in lines]
    best = 0
    for i in range(len(numbers)):
        for j in range(len(numbers)):
            if i == j:
                continue
            result = add(copy.deepcopy(numbers[i]), copy.deepcopy(numbers[j]))
            mag = magnitude(result)
            if mag > best:
                best = mag
    assert best == 3993
