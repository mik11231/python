"""Advent of Code 2018 solution module."""

from pathlib import Path


def load(path: Path):
    """
    Run `load` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    pts = []
    for line in path.read_text().splitlines():
        if line.strip():
            pts.append(tuple(map(int, line.split(','))))
    return pts


def md4(a, b):
    """
    Run `md4` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, b.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return sum(abs(x - y) for x, y in zip(a, b))


def solve(points) -> int:
    """Count constellations via union-find over distance<=3 edges."""
    n = len(points)
    parent = list(range(n))

    def find(x):
        """
        Run `find` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: x.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        """
        Run `union` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: a, b.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for i in range(n):
        for j in range(i + 1, n):
            if md4(points[i], points[j]) <= 3:
                union(i, j)

    return len({find(i) for i in range(n)})


if __name__ == '__main__':
    print(solve(load(Path(__file__).with_name('d25_input.txt'))))
