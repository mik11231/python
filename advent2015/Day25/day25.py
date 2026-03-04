#!/usr/bin/env python3
"""Advent of Code 2015 Day 25 — Let It Snow.

Code at (r,c): first 20151125, then *252533 mod 33554393. Diagonal order.
Find code at given row, col from input.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import ints


def index_of(row: int, col: int) -> int:
    """Return 1-based index in diagonal order: (1,1)=1, (2,1)=2, (1,2)=3, (3,1)=4, ..."""
    # Diagonal d: (d,1), (d-1,2), ..., (1,d). Size of diagonal d is d.
    # Index of (r,c) where r+c = d+1: previous diagonals sum = 1+2+...+(d-1) = d*(d-1)/2
    # Position in diagonal d: col (since row = d+1-col, so (r,c) has r+c = d+1, so d = r+c-1)
    d = row + col - 1
    prev_count = d * (d - 1) // 2
    # In diagonal d, (d,1) is first, (d-1,2) second, ... (1,d) is d-th. (r,c) has c-th position.
    return prev_count + col


def code_at(row: int, col: int) -> int:
    """Return code at (row, col). First code 20151125, then *252533 mod 33554393."""
    idx = index_of(row, col)
    val = 20151125
    mod = 33554393
    mult = 252533
    for _ in range(idx - 1):
        val = (val * mult) % mod
    return val


def solve(s: str) -> int:
    """Parse row and col from input (e.g. 'Enter the code at row 2947, column 3029.'), return code."""
    nums = ints(s)
    if len(nums) >= 2:
        row, col = nums[0], nums[1]
    else:
        row, col = 2947, 3029
    return code_at(row, col)


if __name__ == "__main__":
    text = Path(__file__).with_name("d25_input.txt").read_text(encoding="utf-8")
    print(solve(text))
