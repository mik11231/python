#!/usr/bin/env python3
"""Advent of Code 2023 Day 23 Part 1 - A Long Walk.

Find the longest path through a hiking trail grid, respecting slope directions.
Compress the grid to a graph of junctions and use DFS to find the longest path.
"""
from pathlib import Path
from collections import defaultdict


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

    slope_dirs = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}

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

    graph = defaultdict(list)
    for jr, jc in junctions:
        stack = [(jr, jc, 0)]
        visited = {(jr, jc)}
        while stack:
            r, c, dist = stack.pop()
            if dist > 0 and (r, c) in junctions:
                graph[(jr, jc)].append(((r, c), dist))
                continue
            ch = grid[r][c]
            dirs = [slope_dirs[ch]] if ch in slope_dirs else [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc, dist + 1))

    best = 0
    stack = [(start, 0, frozenset([start]))]
    while stack:
        node, dist, visited = stack.pop()
        if node == end:
            best = max(best, dist)
            continue
        for next_node, edge_dist in graph[node]:
            if next_node not in visited:
                stack.append((next_node, dist + edge_dist, visited | {next_node}))

    return best


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d23_input.txt").read_text()))
