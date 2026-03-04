#!/usr/bin/env python3
"""Advent of Code 2015 Day 12 Part 2 — Ignore objects with value "red".

Sum all numbers in JSON; if any object has a property value "red", skip that object.
"""
import json
from pathlib import Path


def sum_numbers(obj: object) -> int:
    """Recursively sum numbers; skip any object that has a property value 'red'."""
    if isinstance(obj, int):
        return obj
    if isinstance(obj, list):
        return sum(sum_numbers(item) for item in obj)
    if isinstance(obj, dict):
        if "red" in obj.values():
            return 0
        return sum(sum_numbers(v) for v in obj.values())
    return 0


def solve(s: str) -> int:
    """Return sum of numbers, excluding objects with a 'red' value."""
    data = json.loads(s.strip())
    return sum_numbers(data)


if __name__ == "__main__":
    text = Path(__file__).with_name("d12_input.txt").read_text(encoding="utf-8")
    print(solve(text))
