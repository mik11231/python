"""Advent of Code 2019 Day 13 Part 1."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def solve(program):
    vm = IntcodeComputer(program)
    out, _ = vm.run([])
    return sum(1 for i in range(2, len(out), 3) if out[i] == 2)


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d13_input.txt').read_text().strip().split(',')]
    print(solve(p))
