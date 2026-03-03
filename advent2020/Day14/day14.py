#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 14: Docking Data (Part 1)

A 36-bit bitmask system initialises a docking program.  Two kinds of
instructions appear:

  mask = <36-char string of 0/1/X>
  mem[addr] = val

When writing a value, the current mask is applied bit-by-bit:
  0 — forces the bit to 0
  1 — forces the bit to 1
  X — leaves the bit unchanged

Return the sum of all values in memory after the program completes.

Algorithm
---------
Convert the mask into an OR-mask (the 1-bits) and an AND-mask (the inverse
of the 0-bits).  Applying both in sequence gives the correct result:
  value = (value | or_mask) & and_mask
"""

from pathlib import Path
import re

MEM_RE = re.compile(r"mem\[(\d+)] = (\d+)")


def parse_program(text: str) -> list[tuple[str, ...]]:
    """Return a list of ('mask', maskstr) or ('mem', addr, val) tuples."""
    instructions: list[tuple[str, ...]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("mask"):
            instructions.append(("mask", line.split(" = ")[1]))
        else:
            m = MEM_RE.match(line)
            if m:
                instructions.append(("mem", m.group(1), m.group(2)))
    return instructions


def run_v1(program: list[tuple[str, ...]]) -> dict[int, int]:
    """Execute the program with version-1 (value masking) semantics."""
    memory: dict[int, int] = {}
    or_mask = 0
    and_mask = (1 << 36) - 1

    for instr in program:
        if instr[0] == "mask":
            mask_str = instr[1]
            or_mask = int(mask_str.replace("X", "0"), 2)
            and_mask = int(mask_str.replace("X", "1"), 2)
        else:
            addr = int(instr[1])
            val = int(instr[2])
            memory[addr] = (val | or_mask) & and_mask

    return memory


def solve(input_path: str = "advent2020/Day14/d14_input.txt") -> int:
    """Read the docking program and return the sum of all memory values."""
    program = parse_program(Path(input_path).read_text())
    memory = run_v1(program)
    return sum(memory.values())


if __name__ == "__main__":
    result = solve()
    print(f"Sum of all values in memory (v1): {result}")
