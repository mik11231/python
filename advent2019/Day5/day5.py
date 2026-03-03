"""Advent of Code 2019 Day 5 Part 1."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def solve(program: list[int]) -> int:
    vm = IntcodeComputer(program)
    out, _ = vm.run([1])
    return out[-1]


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d5_input.txt').read_text().strip().split(',')]
    print(solve(p))
