#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 14: Extended Polymerization (Part 1)

Given a polymer template and a set of pair insertion rules, each step
simultaneously inserts a character between every adjacent pair that matches
a rule.  After 10 steps, compute the difference between the counts of the
most and least common elements.

Algorithm
---------
Instead of building the actual string (which grows exponentially), maintain
a Counter of adjacent character pairs.  Each step, every pair AB with rule
AB -> C produces pairs AC and CB (each multiplied by the count of AB).
Element frequencies are recovered from pair counts: every character appears
as the left half of some pairs and the right half of others.  Each character
is double-counted except the very first and last characters of the polymer
(which never change), so we add 1 for each endpoint and halve all counts.
"""

from collections import Counter
from pathlib import Path


def parse_input(text: str) -> tuple[str, dict[str, str]]:
    """Parse the polymer template and insertion rules from *text*.

    Returns (template_string, rules_dict) where rules_dict maps e.g. 'CH' -> 'B'.
    """
    blocks = text.strip().split("\n\n")
    template = blocks[0].strip()
    rules: dict[str, str] = {}
    for line in blocks[1].strip().splitlines():
        pair, insert = line.split(" -> ")
        rules[pair.strip()] = insert.strip()
    return template, rules


def polymerize(pair_counts: Counter, rules: dict[str, str], steps: int) -> Counter:
    """Apply *steps* rounds of pair insertion to *pair_counts* using *rules*.

    Returns the resulting pair-count Counter.
    """
    for _ in range(steps):
        new_counts: Counter = Counter()
        for pair, count in pair_counts.items():
            if pair in rules:
                insert = rules[pair]
                new_counts[pair[0] + insert] += count
                new_counts[insert + pair[1]] += count
            else:
                new_counts[pair] += count
        pair_counts = new_counts
    return pair_counts


def element_counts(pair_counts: Counter, first_char: str, last_char: str) -> Counter:
    """Derive element frequencies from *pair_counts*.

    Every character is double-counted (once as the left element of a pair,
    once as the right).  The first and last characters of the polymer are
    each counted one fewer time, so we add 1 for each endpoint and halve.
    """
    counts: Counter = Counter()
    for pair, n in pair_counts.items():
        counts[pair[0]] += n
        counts[pair[1]] += n
    counts[first_char] += 1
    counts[last_char] += 1
    for ch in counts:
        counts[ch] //= 2
    return counts


def solve(input_path: str = "advent2021/Day14/d14_input.txt") -> int:
    """Read puzzle input, run 10 polymerization steps, and return
    most_common - least_common element count."""
    text = Path(input_path).read_text()
    template, rules = parse_input(text)
    pair_counts: Counter = Counter()
    for i in range(len(template) - 1):
        pair_counts[template[i] + template[i + 1]] += 1
    pair_counts = polymerize(pair_counts, rules, 10)
    counts = element_counts(pair_counts, template[0], template[-1])
    ordered = counts.most_common()
    return ordered[0][1] - ordered[-1][1]


if __name__ == "__main__":
    result = solve()
    print(f"Most common minus least common after 10 steps: {result}")
