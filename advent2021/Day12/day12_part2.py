#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 12: Passage Pathing (Part 2)

Same cave graph, but now a single small cave (not ``start`` or ``end``) may
be visited twice.  All other small caves still have a visit limit of one.

Algorithm
---------
Extend the Part 1 DFS with a boolean flag ``double_used`` that tracks
whether the one allowed double-visit has been consumed.  When visiting a
small cave already in the visited set, consume the allowance instead of
skipping, provided the cave is not ``start``.
"""

from pathlib import Path

from day12 import parse_graph


def count_paths_part2(graph: dict[str, list[str]]) -> int:
    """Count paths allowing one small cave (not start/end) to be visited twice."""

    def dfs(node: str, visited: set[str], double_used: bool) -> int:
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: node, visited, double_used.
        - Returns the computed result for this stage of the pipeline.
        """
        if node == "end":
            return 1
        total = 0
        for neighbor in graph.get(node, []):
            if neighbor == "start":
                continue
            if neighbor.islower():
                if neighbor not in visited:
                    visited.add(neighbor)
                    total += dfs(neighbor, visited, double_used)
                    visited.remove(neighbor)
                elif not double_used:
                    total += dfs(neighbor, visited, True)
            else:
                total += dfs(neighbor, visited, double_used)
        return total

    return dfs("start", {"start"}, False)


def solve(input_path: str = "advent2021/Day12/d12_input.txt") -> int:
    """Read the cave graph and return the path count with one allowed double-visit."""
    text = Path(input_path).read_text()
    graph = parse_graph(text)
    return count_paths_part2(graph)


if __name__ == "__main__":
    result = solve()
    print(f"Number of paths (with one double-visit): {result}")
