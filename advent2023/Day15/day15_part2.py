#!/usr/bin/env python3
"""Advent of Code 2023 Day 15 Part 2 - Lens Library.

Process lens operations into 256 boxes.  '=' inserts/replaces a lens,
'-' removes it.  Focusing power = sum of (box+1)*(slot+1)*focal_length.
"""
from pathlib import Path


def hash_algo(s: str) -> int:
    val = 0
    for ch in s:
        val = (val + ord(ch)) * 17 % 256
    return val


def solve(s: str) -> int:
    """Solve the puzzle and return the answer."""
    boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]

    for step in s.strip().split(","):
        if "=" in step:
            label, focal = step.split("=")
            focal_len = int(focal)
            box = hash_algo(label)
            for i, (lbl, _) in enumerate(boxes[box]):
                if lbl == label:
                    boxes[box][i] = (label, focal_len)
                    break
            else:
                boxes[box].append((label, focal_len))
        else:
            label = step[:-1]
            box = hash_algo(label)
            boxes[box] = [(lbl, fl) for lbl, fl in boxes[box] if lbl != label]

    total = 0
    for b, lenses in enumerate(boxes):
        for slot, (_, fl) in enumerate(lenses):
            total += (b + 1) * (slot + 1) * fl
    return total


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d15_input.txt").read_text()))
