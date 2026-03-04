#!/usr/bin/env python3
"""Advent of Code 2024 Day 9 Part 1 - Disk Fragmenter.

Compact a disk by moving individual file blocks from the right end into
the leftmost free space. Two-pointer approach on the expanded block array,
then compute a position-weighted checksum.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return the filesystem checksum after block-level compaction."""
    disk_map = s.strip()
    blocks = []
    file_id = 0
    for i, ch in enumerate(disk_map):
        length = int(ch)
        if i % 2 == 0:
            blocks.extend([file_id] * length)
            file_id += 1
        else:
            blocks.extend([-1] * length)

    left, right = 0, len(blocks) - 1
    while left < right:
        while left < right and blocks[left] != -1:
            left += 1
        while left < right and blocks[right] == -1:
            right -= 1
        if left < right:
            blocks[left], blocks[right] = blocks[right], blocks[left]
            left += 1
            right -= 1

    return sum(i * b for i, b in enumerate(blocks) if b != -1)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d9_input.txt").read_text()))
