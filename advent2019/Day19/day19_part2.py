"""Advent of Code 2019 Day 19 Part 2."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def probe(program, x, y):
    vm = IntcodeComputer(program)
    out, _ = vm.run([x, y])
    return out[-1]


def solve(program):
    x = 0
    for y in range(100, 5000):
        while probe(program, x, y) == 0:
            x += 1
        # Check top-right corner of 100x100 square.
        if probe(program, x + 99, y - 99) == 1:
            return x * 10000 + (y - 99)
    raise RuntimeError('not found')


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d19_input.txt').read_text().strip().split(',')]
    print(solve(p))
