#!/usr/bin/env python3
"""Advent of Code 2024 Day 15 Part 2 - Warehouse Woes (wide grid).

The warehouse is scaled 2x horizontally: walls become ##, boxes become [],
empty becomes .., and the robot @ becomes @. (dot).
Wide boxes can chain-push vertically: a single push up/down may move
multiple boxes in a tree-like cascade. We BFS to find all affected boxes
before committing the move.
"""
from pathlib import Path
from collections import deque


def solve(s: str) -> int:
    """Return sum of GPS coordinates of all wide boxes after simulation."""
    grid_part, moves_part = s.split("\n\n")
    moves = moves_part.replace("\n", "")

    expand = {'#': '##', 'O': '[]', '.': '..', '@': '@.'}
    wide_rows = []
    for row in grid_part.splitlines():
        wide_rows.append(list("".join(expand[ch] for ch in row)))
    grid = wide_rows
    rows, cols = len(grid), len(grid[0])

    rr = rc = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '@':
                rr, rc = r, c
                grid[r][c] = '.'
                break

    dirs = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}

    for m in moves:
        dr, dc = dirs[m]
        nr, nc = rr + dr, rc + dc

        if grid[nr][nc] == '#':
            continue
        if grid[nr][nc] == '.':
            rr, rc = nr, nc
            continue

        if m in '<>':
            # horizontal push: chain of [] along the row
            ec = nc
            while grid[rr][ec] in '[]':
                ec += dc
            if grid[rr][ec] == '#':
                continue
            # shift everything
            while ec != nc:
                grid[rr][ec] = grid[rr][ec - dc]
                ec -= dc
            grid[rr][nc] = '.'
            rr, rc = nr, nc
        else:
            # vertical push: BFS to find all box cells that must move
            boxes = set()
            frontier = deque()
            ch = grid[nr][nc]
            if ch == '[':
                frontier.append((nr, nc))
                frontier.append((nr, nc + 1))
                boxes.add((nr, nc))
                boxes.add((nr, nc + 1))
            else:  # ']'
                frontier.append((nr, nc))
                frontier.append((nr, nc - 1))
                boxes.add((nr, nc))
                boxes.add((nr, nc - 1))

            blocked = False
            while frontier:
                br, bc = frontier.popleft()
                tr, tc = br + dr, bc
                if (tr, tc) in boxes:
                    continue
                ch2 = grid[tr][tc]
                if ch2 == '#':
                    blocked = True
                    break
                if ch2 == '[':
                    boxes.add((tr, tc))
                    boxes.add((tr, tc + 1))
                    frontier.append((tr, tc))
                    frontier.append((tr, tc + 1))
                elif ch2 == ']':
                    boxes.add((tr, tc))
                    boxes.add((tr, tc - 1))
                    frontier.append((tr, tc))
                    frontier.append((tr, tc - 1))

            if blocked:
                continue

            # move boxes: sort so we move in the right order
            sorted_boxes = sorted(boxes, key=lambda p: p[0], reverse=(dr == 1))
            chars = {(br, bc): grid[br][bc] for br, bc in sorted_boxes}
            for br, bc in sorted_boxes:
                grid[br][bc] = '.'
            for br, bc in sorted_boxes:
                grid[br + dr][bc] = chars[(br, bc)]
            rr, rc = nr, nc

    total = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '[':
                total += 100 * r + c
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d15_input.txt").read_text()))
