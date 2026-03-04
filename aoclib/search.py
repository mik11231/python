"""Generic graph search helpers for Advent of Code problems."""

from __future__ import annotations

from collections import deque
import heapq
from typing import Callable, Iterable, TypeVar

T = TypeVar("T")


def bfs_distances(start: T, neighbors: Callable[[T], Iterable[T]]) -> dict[T, int]:
    """Compute shortest unweighted distances from start using BFS."""
    dist: dict[T, int] = {start: 0}
    queue: deque[T] = deque([start])

    while queue:
        node = queue.popleft()
        step = dist[node] + 1
        for nxt in neighbors(node):
            if nxt in dist:
                continue
            dist[nxt] = step
            queue.append(nxt)

    return dist


def dijkstra_distances(
    start: T,
    neighbors: Callable[[T], Iterable[tuple[T, int]]],
) -> dict[T, int]:
    """Compute shortest weighted distances from start using Dijkstra."""
    dist: dict[T, int] = {start: 0}
    heap: list[tuple[int, T]] = [(0, start)]

    while heap:
        cost, node = heapq.heappop(heap)
        if cost != dist.get(node):
            continue
        for nxt, w in neighbors(node):
            new_cost = cost + w
            if new_cost < dist.get(nxt, 10**30):
                dist[nxt] = new_cost
                heapq.heappush(heap, (new_cost, nxt))

    return dist
