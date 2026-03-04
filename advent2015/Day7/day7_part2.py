#!/usr/bin/env python3
"""Advent of Code 2015 Day 7 Part 2 — Override b with Part 1 answer."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from day7 import parse, eval_circuit

def solve(s: str) -> int:
    """Evaluate with b overridden by Part 1 'a' value."""
    circuit = parse(s)
    a1 = eval_circuit(circuit)["a"]
    vals = eval_circuit(circuit, override={"b": a1})
    return vals["a"]


if __name__ == "__main__":
    text = Path(__file__).with_name("d7_input.txt").read_text(encoding="utf-8")
    print(solve(text))
