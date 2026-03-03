#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 7: Handy Haversacks (Part 1)

Luggage rules describe which bags must be carried inside other bags.
The question: how many distinct bag colours can eventually contain at least
one "shiny gold" bag?

Algorithm
---------
1. Parse every rule into a *reverse* mapping:  child_color -> set of parent
   colours that directly contain it.
2. BFS outward from "shiny gold" along the reverse edges, collecting every
   colour reachable.  The count of those colours (excluding shiny gold itself)
   is the answer.
"""

from collections import defaultdict, deque
from pathlib import Path


def parse_rules(lines: list[str]) -> dict[str, list[tuple[int, str]]]:
    """Parse bag rules into {parent_color: [(count, child_color), ...]}."""
    rules: dict[str, list[tuple[int, str]]] = {}
    for line in lines:
        if not line.strip():
            continue
        colour_part, contents_part = line.split(" bags contain ")
        parent = colour_part.strip()
        children: list[tuple[int, str]] = []
        if "no other bags" not in contents_part:
            for item in contents_part.rstrip(".").split(", "):
                words = item.split()
                count = int(words[0])
                child_color = " ".join(words[1:-1])  # drop count and "bag(s)"
                children.append((count, child_color))
        rules[parent] = children
    return rules


def build_reverse_graph(rules: dict[str, list[tuple[int, str]]]) -> dict[str, set[str]]:
    """Build a mapping from each child colour to the set of parent colours
    that directly contain it."""
    reverse: dict[str, set[str]] = defaultdict(set)
    for parent, children in rules.items():
        for _, child_color in children:
            reverse[child_color].add(parent)
    return reverse


def count_containers(rules: dict[str, list[tuple[int, str]]], target: str = "shiny gold") -> int:
    """Return how many distinct colours can eventually contain *target*."""
    reverse = build_reverse_graph(rules)
    visited: set[str] = set()
    queue: deque[str] = deque([target])

    while queue:
        current = queue.popleft()
        for parent in reverse.get(current, set()):
            if parent not in visited:
                visited.add(parent)
                queue.append(parent)

    return len(visited)


def solve(input_path: str = "advent2020/Day7/d7_input.txt") -> int:
    """Read the bag rules and count how many colours can contain shiny gold."""
    lines = Path(input_path).read_text().splitlines()
    rules = parse_rules(lines)
    return count_containers(rules)


if __name__ == "__main__":
    result = solve()
    print(f"Bag colours that can contain shiny gold: {result}")
