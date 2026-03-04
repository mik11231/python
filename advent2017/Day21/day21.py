#!/usr/bin/env python3
"""Advent of Code 2017 Day 21 Part 1."""

from pathlib import Path


def rots(grid: tuple[str, ...]) -> list[tuple[str, ...]]:
    out = []
    g = grid
    for _ in range(4):
        out.append(g)
        n = len(g)
        g = tuple("".join(g[n - 1 - c][r] for c in range(n)) for r in range(n))
    return out


def flips(grid: tuple[str, ...]) -> list[tuple[str, ...]]:
    return [grid, tuple(r[::-1] for r in grid)]


def parse(s: str) -> dict[tuple[str, ...], tuple[str, ...]]:
    m = {}
    for ln in s.splitlines():
        a, b = ln.split(" => ")
        src = tuple(a.split("/"))
        dst = tuple(b.split("/"))
        for f in flips(src):
            for r in rots(f):
                m[r] = dst
    return m


def enhance(grid: tuple[str, ...], rules: dict[tuple[str, ...], tuple[str, ...]]) -> tuple[str, ...]:
    n = len(grid)
    k = 2 if n % 2 == 0 else 3
    blocks = n // k
    out_block = k + 1
    out = ["" for _ in range(blocks * out_block)]
    for br in range(blocks):
        for bc in range(blocks):
            src = tuple(grid[br * k + i][bc * k : bc * k + k] for i in range(k))
            dst = rules[src]
            for i in range(out_block):
                out[br * out_block + i] += dst[i]
    return tuple(out)


def solve(s: str) -> int:
    rules = parse(s)
    g = (".#.", "..#", "###")
    for _ in range(5):
        g = enhance(g, rules)
    return sum(r.count("#") for r in g)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d21_input.txt").read_text(encoding="utf-8")))
