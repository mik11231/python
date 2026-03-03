"""Advent of Code 2019 Day 9 Part 2."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def solve(program: list[int]) -> int:
    vm = IntcodeComputer(program)
    out, _ = vm.run([2])
    return out[-1]


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d9_input.txt').read_text().strip().split(',')]
    print(solve(p))
