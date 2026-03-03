#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 6: Custom Customs (Part 1)

Groups of people are separated by blank lines.  Within each group, every
person's answers are on a separate line, where each character is a question
they answered "yes" to.

For Part 1, count the number of questions to which *anyone* in the group
answered yes (i.e. the union of all individual answer sets), then sum those
counts across all groups.
"""

from pathlib import Path


def count_any_yes(group_text: str) -> int:
    """Return the count of distinct questions anyone in the group answered yes."""
    answers = group_text.replace("\n", "")
    return len(set(answers))


def solve(input_path: str = "advent2020/Day6/d6_input.txt") -> int:
    """Sum the 'anyone yes' counts for every group."""
    text = Path(input_path).read_text().rstrip()
    groups = text.split("\n\n")
    return sum(count_any_yes(g) for g in groups)


if __name__ == "__main__":
    result = solve()
    print(f"Sum of 'anyone yes' counts: {result}")
