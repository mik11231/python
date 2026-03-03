#!/usr/bin/env python3
"""Tests for Day 6 using the example from the problem statement.

Five groups:
    "abc"       -> anyone=3, everyone=3  (one person, 3 questions)
    "a/b/c"     -> anyone=3, everyone=0  (3 people, no overlap)
    "ab/ac"     -> anyone=3, everyone=1  (only 'a' in common)
    "a/a/a/a"   -> anyone=1, everyone=1  (all answered 'a')
    "b"         -> anyone=1, everyone=1  (one person, 1 question)

Part 1 total: 3+3+3+1+1 = 11
Part 2 total: 3+0+1+1+1 = 6
"""

from day6 import count_any_yes
from day6_part2 import count_all_yes

EXAMPLE = "abc\n\na\nb\nc\n\nab\nac\n\na\na\na\na\n\nb"


def test_part1():
    """Verify Part 1: anyone-yes sum across groups is 11."""
    groups = EXAMPLE.split("\n\n")
    counts = [count_any_yes(g) for g in groups]
    assert counts == [3, 3, 3, 1, 1], f"Expected [3,3,3,1,1], got {counts}"
    assert sum(counts) == 11
    print(f"PASS  Part 1: counts={counts}, total={sum(counts)}")


def test_part2():
    """Verify Part 2: everyone-yes sum across groups is 6."""
    groups = EXAMPLE.split("\n\n")
    counts = [count_all_yes(g) for g in groups]
    assert counts == [3, 0, 1, 1, 1], f"Expected [3,0,1,1,1], got {counts}"
    assert sum(counts) == 6
    print(f"PASS  Part 2: counts={counts}, total={sum(counts)}")


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("\nAll Day 6 tests passed!")
