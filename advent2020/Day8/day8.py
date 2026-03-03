#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 8: Handheld Halting (Part 1)

A handheld game console runs a simple instruction set:
  - ``acc +N`` — add N to a global accumulator
  - ``jmp +N`` — jump forward/backward by N instructions
  - ``nop +N`` — do nothing (advance to next instruction)

The boot code enters an infinite loop.  Detect the loop (any instruction
about to execute a second time) and report the accumulator value at that
moment.

Algorithm
---------
Parse the program into a list of (op, arg) tuples.  Walk instructions with
a program counter, recording visited indices in a set.  Stop the instant
we revisit an index.
"""

from pathlib import Path


def parse_program(text: str) -> list[tuple[str, int]]:
    """Parse raw program text into a list of (opcode, argument) pairs."""
    instructions: list[tuple[str, int]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        op, arg = line.split()
        instructions.append((op, int(arg)))
    return instructions


def run_program(program: list[tuple[str, int]]) -> tuple[int, bool]:
    """Execute *program* and return (accumulator, terminated_normally).

    ``terminated_normally`` is True when the program counter advances past
    the last instruction, False when an infinite loop is detected.
    """
    acc = 0
    pc = 0
    visited: set[int] = set()

    while pc < len(program):
        if pc in visited:
            return acc, False
        visited.add(pc)
        op, arg = program[pc]
        if op == "acc":
            acc += arg
            pc += 1
        elif op == "jmp":
            pc += arg
        else:
            pc += 1

    return acc, True


def solve(input_path: str = "advent2020/Day8/d8_input.txt") -> int:
    """Read the boot code, run until a loop is detected, and return the
    accumulator value."""
    program = parse_program(Path(input_path).read_text())
    acc, _ = run_program(program)
    return acc


if __name__ == "__main__":
    result = solve()
    print(f"Accumulator value before the loop: {result}")
