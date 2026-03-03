"""Advent of Code 2018 solution module."""

from collections import defaultdict
from pathlib import Path


def load_edges(path: Path) -> list[tuple[str, str]]:
    edges = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.split()
        edges.append((parts[1], parts[7]))
    return edges


def solve(edges: list[tuple[str, str]]) -> str:
    prereq: dict[str, set[str]] = defaultdict(set)
    nodes = set()
    for a, b in edges:
        prereq[b].add(a)
        nodes.add(a)
        nodes.add(b)
    for n in nodes:
        prereq.setdefault(n, set())

    result = []
    done = set()
    while len(done) < len(nodes):
        ready = sorted(n for n in nodes if n not in done and prereq[n] <= done)
        nxt = ready[0]
        done.add(nxt)
        result.append(nxt)
    return "".join(result)


if __name__ == "__main__":
    print(solve(load_edges(Path(__file__).with_name("d7_input.txt"))))
