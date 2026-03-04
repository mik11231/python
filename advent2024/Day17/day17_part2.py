#!/usr/bin/env python3
"""Advent of Code 2024 Day 17 Part 2 - Chronospatial Computer (quine).

Find the smallest initial value of register A that makes the program
output a copy of itself. The program divides A by 8 each iteration
(via adv with operand 3), so we can reconstruct A 3 bits at a time,
starting from the last output digit and working backwards via DFS.
"""
from pathlib import Path
import re


def run(program, a, b, c):
    """Execute program and return output list."""
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

        if opcode == 0:
            regs[0] >>= combo(operand)
        elif opcode == 1:
            regs[1] ^= operand
        elif opcode == 2:
            regs[1] = combo(operand) & 7
        elif opcode == 3:
            if regs[0] != 0:
                ip = operand
                continue
        elif opcode == 4:
            regs[1] ^= regs[2]
        elif opcode == 5:
            out.append(combo(operand) & 7)
        elif opcode == 6:
            regs[1] = regs[0] >> combo(operand)
        elif opcode == 7:
            regs[2] = regs[0] >> combo(operand)

        ip += 2

    return out


def solve(s: str) -> int:
    """Return the smallest A that causes the program to output itself."""
    nums = list(map(int, re.findall(r'\d+', s)))
    b0, c0 = nums[1], nums[2]
    program = nums[3:]

    def search(pos, a_so_far):
        if pos < 0:
            return a_so_far
        for bits in range(8):
            a_candidate = (a_so_far << 3) | bits
            out = run(program, a_candidate, b0, c0)
            if out and out[0] == program[pos]:
                if len(out) == len(program) - pos:
                    result = search(pos - 1, a_candidate)
                    if result is not None:
                        return result
        return None

    return search(len(program) - 1, 0)


if __name__ == "__main__":
    print(solve(Path(__file__).with_name("d17_input.txt").read_text()))
