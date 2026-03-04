#!/usr/bin/env python3
"""Advent of Code 2023 Day 19 Part 2 - Aplenty.

Instead of individual parts, consider all combinations where each of x,m,a,s
ranges from 1 to 4000.  Split ranges through the workflow rules via DFS,
counting accepted combinations as the product of range sizes.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    workflow_text = s.strip().split("\n\n")[0]

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

    # ranges: dict mapping 'x','m','a','s' -> (lo, hi) inclusive
    def count_accepted(wf: str, ranges: dict[str, tuple[int, int]]) -> int:
        if wf == "R":
            return 0
        if wf == "A":
            result = 1
            for lo, hi in ranges.values():
                result *= hi - lo + 1
            return result

        total = 0
        cur = dict(ranges)

        for var, op, val, dest in workflows[wf]:
            if var is None:
                total += count_accepted(dest, cur)
                break

            lo, hi = cur[var]
            if op == "<":
                if hi < val:
                    total += count_accepted(dest, cur)
                    break
                elif lo < val:
                    match = dict(cur)
                    match[var] = (lo, val - 1)
                    total += count_accepted(dest, match)
                    cur[var] = (val, hi)
            else:  # op == ">"
                if lo > val:
                    total += count_accepted(dest, cur)
                    break
                elif hi > val:
                    match = dict(cur)
                    match[var] = (val + 1, hi)
                    total += count_accepted(dest, match)
                    cur[var] = (lo, val)

        return total

    start_ranges = {v: (1, 4000) for v in "xmas"}
    return count_accepted("in", start_ranges)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d19_input.txt").read_text()))
