#!/usr/bin/env python3
"""Advent of Code 2017 Day 25 Part 2."""

from pathlib import Path


def solve(_: str) -> str:
    return "Merry Christmas"


if __name__ == "__main__":
    _ = Path(__file__).with_name("d25_input.txt").read_text(encoding="utf-8")
    print(solve(""))
