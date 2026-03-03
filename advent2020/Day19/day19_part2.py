#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 19: Monster Messages (Part 2)

Two rules become recursive:
  - ``8: 42`` becomes ``8: 42 | 42 8``  (one-or-more of rule 42)
  - ``11: 42 31`` becomes ``11: 42 31 | 42 11 31``  (balanced repetition)

Algorithm
---------
Pure regex can handle rule 8 (``42+``), but rule 11 requires matching
``42{n} 31{n}`` for the same *n*, which is not regular.

Pragmatic fix: expand rule 11 to a finite alternation up to depth ~10:
  ``42 31 | 42 42 31 31 | ...``
This is safe because messages have finite length.  We rewrite the two rules
in the dict and then call the same ``build_regex`` / ``count_matches``
machinery from Part 1.
"""

from pathlib import Path

from day19 import build_regex, count_matches, parse_rules_and_messages


def _patch_rules(rules: dict[int, str], max_repeat: int = 10) -> dict[int, str]:
    """Return a copy of *rules* with rules 8 and 11 replaced."""
    rules = dict(rules)
    rules[8] = " | ".join(" ".join(["42"] * i) for i in range(1, max_repeat + 1))
    rules[11] = " | ".join(
        " ".join(["42"] * i + ["31"] * i)
        for i in range(1, max_repeat + 1)
    )
    return rules


def solve(input_path: str = "advent2020/Day19/d19_input.txt") -> int:
    """Count messages matching rule 0 with the patched recursive rules."""
    text = Path(input_path).read_text()
    rules, messages = parse_rules_and_messages(text)
    patched = _patch_rules(rules)
    return count_matches(patched, messages)


if __name__ == "__main__":
    result = solve()
    print(f"Messages matching rule 0 (patched): {result}")
