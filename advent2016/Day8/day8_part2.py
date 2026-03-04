#!/usr/bin/env python3
"""Advent of Code 2016 Day 8 Part 2: render code shown on the screen."""

from pathlib import Path


ROWS = 6
COLS = 50
FONT4X6 = {
    ("####", "...#", "..#.", ".#..", "#...", "####"): "Z",
    ("####", "#...", "###.", "#...", "#...", "#..."): "F",
    ("#..#", "#..#", "####", "#..#", "#..#", "#..#"): "H",
    (".###", "#...", "#...", ".##.", "...#", "###."): "S",
    (".##.", "#..#", "#..#", "#..#", "#..#", ".##."): "O",
    (".##.", "#..#", "#...", "#.##", "#..#", ".###"): "G",
    ("###.", "#..#", "#..#", "###.", "#...", "#..."): "P",
}


def run(s: str) -> list[list[bool]]:
    """Execute display instructions and return final screen state."""
    g = [[False] * COLS for _ in range(ROWS)]
    for line in s.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("rect "):
            a, b = map(int, line[5:].split("x"))
            for r in range(b):
                for c in range(a):
                    g[r][c] = True
        elif line.startswith("rotate row y="):
            left, by = line.split(" by ")
            r = int(left.split("=")[1])
            k = int(by) % COLS
            g[r] = g[r][-k:] + g[r][:-k]
        elif line.startswith("rotate column x="):
            left, by = line.split(" by ")
            c = int(left.split("=")[1])
            k = int(by) % ROWS
            col = [g[r][c] for r in range(ROWS)]
            col = col[-k:] + col[:-k]
            for r in range(ROWS):
                g[r][c] = col[r]
    return g


def solve(s: str) -> str:
    """Return decoded CRT text (4x6 AoC font), falling back to raw pixels."""
    g = run(s)
    rows = ["".join("#" if x else "." for x in row) for row in g]
    letters: list[str] = []
    for start in range(0, COLS, 5):
        block = tuple(row[start : start + 4] for row in rows)
        ch = FONT4X6.get(block)
        if ch is None:
            return "\n".join(rows)
        letters.append(ch)
    return "".join(letters)


if __name__ == "__main__":
    text = Path(__file__).with_name("d8_input.txt").read_text(encoding="utf-8")
    print(solve(text))
