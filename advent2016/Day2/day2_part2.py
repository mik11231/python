#!/usr/bin/env python3
"""Advent of Code 2016 Day 2 Part 2: diamond keypad."""

from pathlib import Path


PAD = {
    (0, 2): "1",
    (1, 1): "2", (1, 2): "3", (1, 3): "4",
    (2, 0): "5", (2, 1): "6", (2, 2): "7", (2, 3): "8", (2, 4): "9",
    (3, 1): "A", (3, 2): "B", (3, 3): "C",
    (4, 2): "D",
}


def solve(s: str) -> str:
    """Return bathroom code on the irregular keypad."""
    r, c = 2, 0  # 5
    code: list[str] = []
    for line in s.splitlines():
        for ch in line.strip():
            nr, nc = r, c
            if ch == "U":
                nr -= 1
            elif ch == "D":
                nr += 1
            elif ch == "L":
                nc -= 1
            elif ch == "R":
                nc += 1
            if (nr, nc) in PAD:
                r, c = nr, nc
        code.append(PAD[(r, c)])
    return "".join(code)


if __name__ == "__main__":
    text = Path(__file__).with_name("d2_input.txt").read_text(encoding="utf-8")
    print(solve(text))
