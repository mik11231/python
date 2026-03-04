#!/usr/bin/env python3
"""Advent of Code 2023 Day 25 Part 1 - Snowverload.

Find 3 edges to cut to split the graph into two components.
Uses edge betweenness: BFS from many nodes to find the most-traversed
edges, remove the top 3, then compute component sizes.
"""
from pathlib import Path
from collections import defaultdict, deque
import random


def solve(s: str) -> int:
    graph = defaultdict(set)
    for line in s.strip().splitlines():
        left, right = line.split(": ")
        for r in right.split():
            graph[left].add(r)
            graph[r].add(left)

    nodes = list(graph.keys())
    edge_count = defaultdict(int)

    random.seed(42)
    sample = random.sample(nodes, min(len(nodes), 50))

    for start in sample:
        visited = {start}
        parent = {}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    queue.append(neighbor)

        for node in nodes:
            if node == start or node not in parent:
                continue
            curr = node
            while curr != start:
                prev = parent[curr]
                edge = (min(curr, prev), max(curr, prev))
                edge_count[edge] += 1
                curr = prev

    top_edges = sorted(edge_count, key=edge_count.get, reverse=True)[:3]

    for a, b in top_edges:
        graph[a].discard(b)
        graph[b].discard(a)

    start = nodes[0]
    visited = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return len(visited) * (len(nodes) - len(visited))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d25_input.txt").read_text()))
