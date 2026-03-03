#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 8: Handheld Halting (Part 2)

Exactly one ``jmp`` should be a ``nop``, or one ``nop`` should be a ``jmp``.
Find the single swap that lets the program terminate normally (PC moves past
the last instruction) and return the accumulator after successful termination.

Algorithm
---------
Brute-force each candidate swap: walk through the program and, at every
``jmp`` or ``nop``, try toggling it and re-running.  Because the program is
short (< 700 instructions) the total work is negligible.
"""

from pathlib import Path

from day8 import parse_program, run_program


def find_fix(program: list[tuple[str, int]]) -> int:
    """Try every jmp<->nop swap until the program terminates normally.
    Return the accumulator of the successfully fixed run."""
    swap = {"jmp": "nop", "nop": "jmp"}

    for idx, (op, arg) in enumerate(program):
        if op not in swap:
            continue
        patched = list(program)
        patched[idx] = (swap[op], arg)
        acc, terminated = run_program(patched)
        if terminated:
            return acc

    raise RuntimeError("No single jmp/nop swap fixes the program")


def solve(input_path: str = "advent2020/Day8/d8_input.txt") -> int:
    """Read the boot code, find the one instruction to fix, and return
    the accumulator after the fixed program terminates."""
    program = parse_program(Path(input_path).read_text())
    return find_fix(program)


if __name__ == "__main__":
    result = solve()
    print(f"Accumulator after the fixed program terminates: {result}")
