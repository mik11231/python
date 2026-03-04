#!/usr/bin/env python3
"""Advent of Code 2016 Day 25 Part 2: no separate computational puzzle."""

from pathlib import Path


def solve(_: str) -> str:
    """Return celebratory message for final star."""
    return "Merry Christmas"


if __name__ == "__main__":
    _ = Path(__file__).with_name("d25_input.txt").read_text(encoding="utf-8")
    print(solve(""))
