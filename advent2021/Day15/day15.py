#!/usr/bin/env python3
"""
Advent of Code 2021 - Day 15: Chiton (Part 1)

Find the path from the top-left to the bottom-right of a risk-level grid
that minimises the total risk (the sum of risk values of every cell entered,
excluding the starting cell).

Algorithm
---------
Dijkstra's shortest-path algorithm on a 2-D grid with non-negative edge
weights.  Each cell is a node; edges connect it to its four cardinal
neighbours with weight equal to the destination cell's risk level.  A
min-heap (priority queue) always expands the lowest-cost frontier node.
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.grid import neighbors4
from aoclib.search import dijkstra_distances


def parse_grid(text: str) -> list[list[int]]:
    """Parse a grid of single-digit risk levels from *text*."""
    return [[int(ch) for ch in line] for line in text.strip().splitlines()]


def dijkstra(grid: list[list[int]]) -> int:
    """Return the minimum total risk from top-left to bottom-right of *grid*."""
    rows, cols = len(grid), len(grid[0])
    start = (0, 0)
    target = (rows - 1, cols - 1)

    def _neighbors(cell: tuple[int, int]):
        """
        Run `_neighbors` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: cell.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        r, c = cell
        for nr, nc in neighbors4(r, c, rows, cols):
            yield (nr, nc), grid[nr][nc]

    dist = dijkstra_distances(start, _neighbors)
    return dist[target]


def solve(input_path: str = "advent2021/Day15/d15_input.txt") -> int:
    """Read puzzle input and return the lowest total risk path cost."""
    grid = parse_grid(Path(input_path).read_text())
    return dijkstra(grid)


if __name__ == "__main__":
    result = solve()
    print(f"Lowest total risk: {result}")
