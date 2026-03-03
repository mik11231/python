"""Advent of Code 2019 Day 19 Part 1."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def probe(program, x, y):
    vm = IntcodeComputer(program)
    out, _ = vm.run([x, y])
    return out[-1]


def solve(program):
    return sum(probe(program, x, y) for y in range(50) for x in range(50))


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d19_input.txt').read_text().strip().split(',')]
    print(solve(p))
