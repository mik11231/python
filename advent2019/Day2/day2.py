"""Advent of Code 2019 Day 2 Part 1."""

from pathlib import Path


def run(mem: list[int]) -> list[int]:
    ip = 0
    while True:
        op = mem[ip]
        if op == 99:
            return mem
        a, b, c = mem[ip + 1], mem[ip + 2], mem[ip + 3]
        if op == 1:
            mem[c] = mem[a] + mem[b]
        elif op == 2:
            mem[c] = mem[a] * mem[b]
        else:
            raise ValueError(op)
        ip += 4


def solve(program: list[int]) -> int:
    mem = program.copy()
    mem[1] = 12
    mem[2] = 2
    return run(mem)[0]


if __name__ == '__main__':
    program = [int(x) for x in Path(__file__).with_name('d2_input.txt').read_text().strip().split(',')]
    print(solve(program))
