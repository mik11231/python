#!/usr/bin/env python3
"""Advent of Code 2015 Day 12 — JSAbacusFramework.io.

Sum all numbers in the JSON (Part 1: every number).
"""
import json
from pathlib import Path


def sum_numbers(obj: object) -> int:
    """Recursively sum all numbers in JSON-like structure."""
    if isinstance(obj, int):
        return obj
    if isinstance(obj, list):
        return sum(sum_numbers(item) for item in obj)
    if isinstance(obj, dict):
        return sum(sum_numbers(v) for v in obj.values())
    return 0


def solve(s: str) -> int:
    """Return sum of every number in the JSON."""
    data = json.loads(s.strip())
    return sum_numbers(data)


if __name__ == "__main__":
    text = Path(__file__).with_name("d12_input.txt").read_text(encoding="utf-8")
    print(solve(text))
