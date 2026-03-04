#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 12: Passage Pathing (Part 1)

An undirected graph of caves.  Big caves (uppercase names) can be revisited
any number of times; small caves (lowercase names) may be visited at most
once per path.  Count all distinct paths from ``start`` to ``end``.

Algorithm
---------
DFS with a set tracking visited small caves.  Big caves are never added to
the visited set.  Backtrack after each recursive call by removing the cave
from visited.  Exponential in the worst case but fast on AoC-sized inputs.
"""

from collections import defaultdict
from pathlib import Path


def parse_graph(text: str) -> dict[str, list[str]]:
    """Build an adjacency list from the edge descriptions."""
    graph: dict[str, list[str]] = defaultdict(list)
    for line in text.splitlines():
        if not line.strip():
            continue
        a, b = line.strip().split("-")
        graph[a].append(b)
        graph[b].append(a)
    return dict(graph)


def count_paths(graph: dict[str, list[str]]) -> int:
    """Count all start→end paths visiting small caves at most once."""

    def dfs(node: str, visited: set[str]) -> int:
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: node, visited.
        - Returns the computed result for this stage of the pipeline.
        """
        if node == "end":
            return 1
        total = 0
        for neighbor in graph.get(node, []):
            if neighbor in visited:
                continue
            if neighbor.islower():
                visited.add(neighbor)
                total += dfs(neighbor, visited)
                visited.remove(neighbor)
            else:
                total += dfs(neighbor, visited)
        return total

    return dfs("start", {"start"})


def solve(input_path: str = "advent2021/Day12/d12_input.txt") -> int:
    """Read the cave graph and return the number of paths."""
    text = Path(input_path).read_text()
    graph = parse_graph(text)
    return count_paths(graph)


if __name__ == "__main__":
    result = solve()
    print(f"Number of paths: {result}")
