"""Advent of Code 2018 solution module."""

import heapq
from pathlib import Path

from day22 import load, make_erosion


# Region type from erosion % 3:
# 0 rocky: torch/climbing
# 1 wet: climbing/neither
# 2 narrow: torch/neither
ALLOWED = {
    0: {'torch', 'climbing'},
    1: {'climbing', 'neither'},
    2: {'torch', 'neither'},
}


def solve(depth: int, tx: int, ty: int) -> int:
    erosion = make_erosion(depth, tx, ty)

    def region(x: int, y: int) -> int:
        return erosion(x, y) % 3

    # Dijkstra over (x, y, tool). Start with torch; goal is target with torch.
    start = (0, 0, 'torch')
    goal = (tx, ty, 'torch')

    # Conservative bounds large enough for optimal path around target.
    max_x = tx + 80
    max_y = ty + 80

    pq = [(0, start)]
    dist = {start: 0}

    while pq:
        cost, state = heapq.heappop(pq)
        if cost != dist.get(state):
            continue
        if state == goal:
            return cost

        x, y, tool = state
        r = region(x, y)

        # Tool switch at same coordinate costs +7.
        for nt in ALLOWED[r]:
            if nt == tool:
                continue
            ns = (x, y, nt)
            nc = cost + 7
            if nc < dist.get(ns, 10**18):
                dist[ns] = nc
                heapq.heappush(pq, (nc, ns))

        # Move to adjacent cell (cost +1) if current tool is allowed in destination.
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if nx < 0 or ny < 0 or nx > max_x or ny > max_y:
                continue
            if tool not in ALLOWED[region(nx, ny)]:
                continue
            ns = (nx, ny, tool)
            nc = cost + 1
            if nc < dist.get(ns, 10**18):
                dist[ns] = nc
                heapq.heappush(pq, (nc, ns))

    raise RuntimeError('No path found')


if __name__ == '__main__':
    d, tx, ty = load(Path(__file__).with_name('d22_input.txt'))
    print(solve(d, tx, ty))
