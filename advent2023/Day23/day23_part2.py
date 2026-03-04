#!/usr/bin/env python3
"""Advent of Code 2023 Day 23 Part 2 - A Long Walk.

Longest path ignoring slope restrictions. Compress the grid to a graph of
junctions, then recursive DFS with bitmask for visited nodes.
"""
from pathlib import Path
from collections import defaultdict
import sys


def solve(s: str) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Returns the computed result for this stage of the pipeline.
    """
    grid = s.strip().splitlines()
    rows, cols = len(grid), len(grid[0])
    start = (0, grid[0].index("."))
    end = (rows - 1, grid[rows - 1].index("."))

    junctions = {start, end}
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "#":
                continue
            neighbors = sum(
                1
                for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))
                if 0 <= r + dr < rows and 0 <= c + dc < cols and grid[r + dr][c + dc] != "#"
            )
            if neighbors >= 3:
                junctions.add((r, c))

    junction_list = list(junctions)
    junction_id = {j: i for i, j in enumerate(junction_list)}
    start_id = junction_id[start]
    end_id = junction_id[end]

    adj = [[] for _ in range(len(junction_list))]
    for jr, jc in junctions:
        stack = [(jr, jc, 0)]
        visited = {(jr, jc)}
        while stack:
            r, c, dist = stack.pop()
            if dist > 0 and (r, c) in junctions:
                adj[junction_id[(jr, jc)]].append((junction_id[(r, c)], dist))
                continue
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc, dist + 1))

    sys.setrecursionlimit(10000)
    best = [0]

    def dfs(node, dist, mask):
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: node, dist, mask.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        if node == end_id:
            if dist > best[0]:
                best[0] = dist
            return
        for next_node, edge_dist in adj[node]:
            if not (mask & (1 << next_node)):
                dfs(next_node, dist + edge_dist, mask | (1 << next_node))

    dfs(start_id, 0, 1 << start_id)
    return best[0]


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d23_input.txt").read_text()))
