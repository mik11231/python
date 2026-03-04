#!/usr/bin/env python3
"""Advent of Code 2024 Day 9 Part 2 - Disk Fragmenter.

Compact by moving whole files (highest ID first) into the leftmost gap
that fits. Track file positions and gap segments, then compute checksum
using arithmetic sum formula.
"""
from pathlib import Path


def solve(s: str) -> int:
    """Return the filesystem checksum after whole-file compaction."""
    disk_map = s.strip()
    files = []
    gaps = []
    pos = 0
    file_id = 0
    for i, ch in enumerate(disk_map):
        length = int(ch)
        if i % 2 == 0:
            files.append([pos, length, file_id])
            file_id += 1
        else:
            if length > 0:
                gaps.append([pos, length])
        pos += length

    for fi in range(len(files) - 1, -1, -1):
        fstart, flen, fid = files[fi]
        if flen == 0:
            continue
        for gi in range(len(gaps)):
            gstart, glen = gaps[gi]
            if gstart >= fstart:
                break
            if glen >= flen:
                files[fi][0] = gstart
                if glen == flen:
                    gaps.pop(gi)
                else:
                    gaps[gi][0] = gstart + flen
                    gaps[gi][1] = glen - flen
                break

    checksum = 0
    for fstart, flen, fid in files:
        checksum += fid * (fstart * flen + flen * (flen - 1) // 2)
    return checksum


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d9_input.txt").read_text()))
