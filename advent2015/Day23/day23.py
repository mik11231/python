#!/usr/bin/env python3
"""Advent of Code 2015 Day 23 — Opening the Turing Lock.

Instructions: hlf r, tpl r, inc r, jmp offset, jie r offset, jio r offset.
a=0, b=0. Return value of b when program terminates.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.parsing import lines


def parse_program(s: str) -> list[tuple[str, ...]]:
    """Return list of (op, arg1, arg2_or_none)."""
    prog = []
    for line in lines(s):
        line = line.strip().rstrip(",")
        parts = line.replace(",", " ").split()
        if parts[0] == "jmp":
            prog.append((parts[0], int(parts[1]), None))
        elif parts[0] in ("jie", "jio"):
            prog.append((parts[0], parts[1], int(parts[2])))
        else:
            prog.append((parts[0], parts[1], None))
    return prog


def run(prog: list[tuple], a: int = 0, b: int = 0) -> int:
    """Run program; return b when execution goes past last instruction."""
    regs = {"a": a, "b": b}
    pc = 0
    while 0 <= pc < len(prog):
        op, x, y = prog[pc]
        if op == "hlf":
            regs[x] //= 2
            pc += 1
        elif op == "tpl":
            regs[x] *= 3
            pc += 1
        elif op == "inc":
            regs[x] += 1
            pc += 1
        elif op == "jmp":
            pc += x
        elif op == "jie":
            pc += y if regs[x] % 2 == 0 else 1
        elif op == "jio":
            pc += y if regs[x] == 1 else 1
    return regs["b"]


def solve(s: str) -> int:
    """Return value of register b when program terminates (a=0, b=0)."""
    prog = parse_program(s)
    return run(prog, a=0, b=0)


if __name__ == "__main__":
    text = Path(__file__).with_name("d23_input.txt").read_text(encoding="utf-8")
    print(solve(text))
