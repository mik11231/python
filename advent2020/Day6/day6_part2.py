#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 6: Custom Customs (Part 2)

For Part 2, count the number of questions to which *everyone* in the group
answered yes (i.e. the intersection of all individual answer sets), then sum
those counts across all groups.
"""

from pathlib import Path


def count_all_yes(group_text: str) -> int:
    """Return the count of questions every person in the group answered yes."""
    people = [set(person) for person in group_text.strip().split("\n") if person]
    if not people:
        return 0
    common = people[0]
    for person_set in people[1:]:
        common &= person_set
    return len(common)


def solve(input_path: str = "advent2020/Day6/d6_input.txt") -> int:
    """Sum the 'everyone yes' counts for every group."""
    text = Path(input_path).read_text().rstrip()
    groups = text.split("\n\n")
    return sum(count_all_yes(g) for g in groups)


if __name__ == "__main__":
    result = solve()
    print(f"Sum of 'everyone yes' counts: {result}")
