"""Advent of Code 2018 solution module."""

from collections import defaultdict, deque
from pathlib import Path


DIR = {'N': (0, -1), 'S': (0, 1), 'W': (-1, 0), 'E': (1, 0)}


def load_regex(path: Path) -> str:
    """
    Run `load_regex` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    return path.read_text().strip()


def build_graph(regex: str):
    """Build undirected room graph from regex path expression."""
    graph = defaultdict(set)
    cur = {(0, 0)}
    stack = []  # entries: (branch_start_positions, accumulated_branch_end_positions)

    for ch in regex[1:-1]:  # strip ^ and $
        if ch in DIR:
            dx, dy = DIR[ch]
            nxt = set()
            for x, y in cur:
                nx, ny = x + dx, y + dy
                graph[(x, y)].add((nx, ny))
                graph[(nx, ny)].add((x, y))
                nxt.add((nx, ny))
            cur = nxt
        elif ch == '(':
            stack.append((set(cur), set()))
        elif ch == '|':
            start, acc = stack[-1]
            acc.update(cur)
            stack[-1] = (start, acc)
            cur = set(start)
        elif ch == ')':
            start, acc = stack.pop()
            acc.update(cur)
            cur = acc
        else:
            raise ValueError(ch)

    return graph


def distances(graph, start=(0, 0)):
    """
    Run `distances` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: graph, start.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    dist = {start: 0}
    q = deque([start])
    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def solve(regex: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: regex.
    - Returns the computed result for this stage of the pipeline.
    """
    d = distances(build_graph(regex))
    return max(d.values())


if __name__ == '__main__':
    print(solve(load_regex(Path(__file__).with_name('d20_input.txt'))))
