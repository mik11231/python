#!/usr/bin/env python3
"""Advent of Code 2025 - Day 11: Reactor (Part 1)."""



from pathlib import Path
def parse_graph(lines: list[str]) -> dict[str, list[str]]:
    """Parse `name: dst1 dst2 ...` lines into an adjacency list."""
    graph: dict[str, list[str]] = {}

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"Invalid line (missing ':'): {line}")

        node, rhs = line.split(":", 1)
        node = node.strip()
        outputs = rhs.strip().split() if rhs.strip() else []
        graph[node] = outputs

    return graph


def count_paths_you_to_out(graph: dict[str, list[str]]) -> int:
    """
    Count directed paths from `you` to `out`.

    Assumes paths are finite; if a cycle is reachable from `you` during search,
    this function raises a ValueError.
    """
    if "you" not in graph:
        return 0

    memo: dict[str, int] = {}
    visiting: set[str] = set()

    def dfs(node: str) -> int:
        if node == "out":
            return 1
        if node in memo:
            return memo[node]
        if node in visiting:
            raise ValueError(f"Cycle detected while exploring from 'you': includes '{node}'")

        visiting.add(node)
        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt)
        visiting.remove(node)
        memo[node] = total
        return total

    return dfs("you")


def solve() -> int:
    """Solve Day 11 Part 1 using the real puzzle input."""
    input_path = Path(__file__).with_name('d11_input.txt')
    with input_path.open("r", encoding="utf-8") as f:
        graph = parse_graph(f.readlines())
    return count_paths_you_to_out(graph)


if __name__ == "__main__":
    result = solve()
    print(f"Different paths from you to out: {result}")
