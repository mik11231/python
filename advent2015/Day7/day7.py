#!/usr/bin/env python3
"""Advent of Code 2015 Day 7 — Some Assembly Required.

Evaluate wire circuit: AND, OR, LSHIFT, RSHIFT, NOT, direct. 16-bit values.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


def parse(s: str) -> dict[str, list[str]]:
    """Return wire -> [op, arg1?, arg2?] for each assignment."""
    circuit: dict[str, list[str]] = {}
    for line in lines(s):
        m = re.match(r"(.+)\s+->\s+(\w+)$", line.strip())
        if not m:
            continue
        expr, out = m.group(1), m.group(2)
        parts = expr.split()
        if len(parts) == 1:
            circuit[out] = ["VAL", parts[0]]
        elif len(parts) == 2 and parts[0] == "NOT":
            circuit[out] = ["NOT", parts[1]]
        elif len(parts) == 3:
            circuit[out] = [parts[1], parts[0], parts[2]]
        else:
            continue
    return circuit


def eval_circuit(circuit: dict[str, list[str]], override: dict[str, int] | None = None) -> dict[str, int]:
    """Evaluate in dependency order; 16-bit unsigned."""
    vals: dict[str, int] = dict(override or {})

    def get(x: str) -> int:
        """
        Run `get` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: x.
        - Returns the computed result for this stage of the pipeline.
        """
        if x.isdigit():
            return int(x)
        if x in vals:
            return vals[x]
        op = circuit[x]
        if op[0] == "VAL":
            v = get(op[1])
        elif op[0] == "NOT":
            v = (~get(op[1])) & 0xFFFF
        elif op[0] == "AND":
            v = (get(op[1]) & get(op[2])) & 0xFFFF
        elif op[0] == "OR":
            v = (get(op[1]) | get(op[2])) & 0xFFFF
        elif op[0] == "LSHIFT":
            v = (get(op[1]) << int(op[2])) & 0xFFFF
        elif op[0] == "RSHIFT":
            v = (get(op[1]) >> int(op[2])) & 0xFFFF
        else:
            raise ValueError(op)
        vals[x] = v
        return v

    for w in circuit:
        if w not in vals:
            get(w)
    return vals


def solve(s: str) -> int:
    """Return value of wire 'a'."""
    circuit = parse(s)
    vals = eval_circuit(circuit)
    return vals["a"]


if __name__ == "__main__":
    text = Path(__file__).with_name("d7_input.txt").read_text(encoding="utf-8")
    print(solve(text))
