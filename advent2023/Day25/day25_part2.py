#!/usr/bin/env python3
"""Advent of Code 2023 Day 25 Part 2 - Snowverload.

Day 25 Part 2 is the free star for completing all other puzzles.
"""
from pathlib import Path


def solve(s: str) -> str:
    return "Merry Christmas!"


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d25_input.txt").read_text()))
