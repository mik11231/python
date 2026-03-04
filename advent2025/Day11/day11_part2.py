#!/usr/bin/env python3
"""Advent of Code 2025 - Day 11: Reactor (Part 2)."""



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


def count_paths_with_required_nodes(
    graph: dict[str, list[str]],
    start: str,
    end: str,
    required_nodes: tuple[str, ...],
) -> int:
    """
    Count directed paths from `start` to `end` that visit all `required_nodes`.

    Raises ValueError if a cycle is encountered while exploring state-space.
    """
    req_index = {name: i for i, name in enumerate(required_nodes)}
    full_mask = (1 << len(required_nodes)) - 1

    def mark(mask: int, node: str) -> int:
        idx = req_index.get(node)
        if idx is None:
            return mask
        return mask | (1 << idx)

    start_mask = mark(0, start)
    memo: dict[tuple[str, int], int] = {}
    visiting: set[tuple[str, int]] = set()

    def dfs(node: str, mask: int) -> int:
        state = (node, mask)
        if node == end:
            return 1 if mask == full_mask else 0
        if state in memo:
            return memo[state]
        if state in visiting:
            raise ValueError(f"Cycle detected while exploring state {state}")

        visiting.add(state)
        total = 0
        for nxt in graph.get(node, []):
            total += dfs(nxt, mark(mask, nxt))
        visiting.remove(state)
        memo[state] = total
        return total

    return dfs(start, start_mask)


def solve() -> int:
    """Solve Day 11 Part 2 using the real puzzle input."""
    input_path = Path(__file__).with_name('d11_input.txt')
    with input_path.open("r", encoding="utf-8") as f:
        graph = parse_graph(f.readlines())
    return count_paths_with_required_nodes(graph, "svr", "out", ("dac", "fft"))


if __name__ == "__main__":
    result = solve()
    print(f"Paths from svr to out that visit dac and fft: {result}")
