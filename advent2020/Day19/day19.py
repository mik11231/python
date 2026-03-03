#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 19: Monster Messages (Part 1)

Input has numbered grammar rules and a list of messages.  Rules are either a
literal character (``4: "a"``) or sequences of rule references separated by
``|`` for alternatives (``0: 1 2 | 3 4``).  Count messages that completely
match rule 0.

Algorithm
---------
Build a regex from the rules by recursively expanding each rule reference.
Since Part 1 rules form a non-recursive CFG this always terminates.  Anchor
the final pattern with ``^...$`` and test each message.
"""

import re
from pathlib import Path


def parse_rules_and_messages(text: str) -> tuple[dict[int, str], list[str]]:
    """Split the puzzle input into raw rule strings and message lines."""
    sections = text.strip().split("\n\n")
    rules: dict[int, str] = {}
    for line in sections[0].splitlines():
        idx_s, body = line.split(": ", 1)
        rules[int(idx_s)] = body
    messages = sections[1].splitlines()
    return rules, messages


def build_regex(rules: dict[int, str], rule_id: int = 0, depth: int = 0, max_depth: int = 50) -> str:
    """Recursively convert rule *rule_id* into a regex pattern string.

    *max_depth* guards against infinite recursion for Part 2's modified rules.
    """
    if depth > max_depth:
        return ""

    body = rules[rule_id]

    literal = re.match(r'"(.)"', body)
    if literal:
        return re.escape(literal.group(1))

    alternatives = body.split(" | ")
    parts: list[str] = []
    for alt in alternatives:
        seq = "".join(
            build_regex(rules, int(ref), depth + 1, max_depth)
            for ref in alt.split()
        )
        parts.append(seq)

    if len(parts) == 1:
        return parts[0]
    return "(?:" + "|".join(parts) + ")"


def count_matches(rules: dict[int, str], messages: list[str]) -> int:
    """Return how many messages fully match rule 0."""
    pattern = re.compile("^" + build_regex(rules) + "$")
    return sum(1 for msg in messages if pattern.match(msg))


def solve(input_path: str = "advent2020/Day19/d19_input.txt") -> int:
    """Count messages matching rule 0."""
    text = Path(input_path).read_text()
    rules, messages = parse_rules_and_messages(text)
    return count_matches(rules, messages)


if __name__ == "__main__":
    result = solve()
    print(f"Messages matching rule 0: {result}")
