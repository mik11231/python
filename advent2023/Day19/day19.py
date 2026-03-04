#!/usr/bin/env python3
"""Advent of Code 2023 Day 19 Part 1 - Aplenty.

Parse workflows and parts.  Send each part through workflows starting at 'in',
evaluating rules until it reaches 'A' (accepted) or 'R' (rejected).
Sum x+m+a+s for all accepted parts.
"""
from pathlib import Path
import re


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    workflow_text, parts_text = s.strip().split("\n\n")

    workflows: dict[str, list[tuple]] = {}
    for line in workflow_text.splitlines():
        name, rest = line.split("{")
        rest = rest.rstrip("}")
        rules = []
        for rule in rest.split(","):
            if ":" in rule:
                cond, dest = rule.split(":")
                var = cond[0]
                op = cond[1]
                val = int(cond[2:])
                rules.append((var, op, val, dest))
            else:
                rules.append((None, None, None, rule))
        workflows[name] = rules

    total = 0
    for part_str in parts_text.splitlines():
        nums = list(map(int, re.findall(r"\d+", part_str)))
        part = {"x": nums[0], "m": nums[1], "a": nums[2], "s": nums[3]}

        wf = "in"
        while wf not in ("A", "R"):
            for var, op, val, dest in workflows[wf]:
                if var is None:
                    wf = dest
                    break
                if op == "<" and part[var] < val:
                    wf = dest
                    break
                if op == ">" and part[var] > val:
                    wf = dest
                    break

        if wf == "A":
            total += sum(part.values())

    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d19_input.txt").read_text()))
