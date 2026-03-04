"""Advent of Code 2018 solution module."""

from collections import defaultdict
from pathlib import Path


def load_edges(path: Path) -> list[tuple[str, str]]:
    """
    Run `load_edges` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    edges = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        parts = line.split()
        edges.append((parts[1], parts[7]))
    return edges


def solve(edges: list[tuple[str, str]], workers: int = 5, base: int = 60) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: edges, workers, base.
    - Returns the computed result for this stage of the pipeline.
    """
    prereq: dict[str, set[str]] = defaultdict(set)
    nodes = set()
    for a, b in edges:
        prereq[b].add(a)
        nodes.add(a)
        nodes.add(b)
    for n in nodes:
        prereq.setdefault(n, set())

    time = 0
    done = set()
    in_progress: dict[str, int] = {}

    while len(done) < len(nodes):
        finished = [task for task, t_end in in_progress.items() if t_end == time]
        for task in finished:
            done.add(task)
            del in_progress[task]

        available = sorted(
            n for n in nodes if n not in done and n not in in_progress and prereq[n] <= done
        )
        while available and len(in_progress) < workers:
            task = available.pop(0)
            duration = base + (ord(task) - ord("A") + 1)
            in_progress[task] = time + duration

        if len(done) == len(nodes):
            break
        time = min(in_progress.values())

    return time


if __name__ == "__main__":
    print(solve(load_edges(Path(__file__).with_name("d7_input.txt")), workers=5, base=60))
