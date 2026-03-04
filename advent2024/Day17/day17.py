#!/usr/bin/env python3
"""Advent of Code 2024 Day 17 Part 1 - Chronospatial Computer.

Simulate a 3-bit computer with registers A, B, C and 8 opcodes.
Run the program and collect all output values, joined by commas.
"""
from pathlib import Path
import re


def run(program, a, b, c):
    """Execute program with given registers, return list of output ints."""
    regs = [a, b, c]
    ip = 0
    out = []

    def combo(op):
        if op <= 3:
            return op
        return regs[op - 4]

    while ip < len(program):
        opcode = program[ip]
        operand = program[ip + 1]

        if opcode == 0:    # adv
            regs[0] >>= combo(operand)
        elif opcode == 1:  # bxl
            regs[1] ^= operand
        elif opcode == 2:  # bst
            regs[1] = combo(operand) & 7
        elif opcode == 3:  # jnz
            if regs[0] != 0:
                ip = operand
                continue
        elif opcode == 4:  # bxc
            regs[1] ^= regs[2]
        elif opcode == 5:  # out
            out.append(combo(operand) & 7)
        elif opcode == 6:  # bdv
            regs[1] = regs[0] >> combo(operand)
        elif opcode == 7:  # cdv
            regs[2] = regs[0] >> combo(operand)

        ip += 2

    return out


def solve(s: str) -> str:
    """Return the comma-separated output of the program."""
    nums = list(map(int, re.findall(r'\d+', s)))
    a, b, c = nums[0], nums[1], nums[2]
    program = nums[3:]
    return ",".join(map(str, run(program, a, b, c)))


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d17_input.txt").read_text()))
