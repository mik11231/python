"""Advent of Code 2019 Day 21 Part 2."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def run_script(program, lines):
    vm = IntcodeComputer(program)
    inp = [ord(c) for c in '\n'.join(lines) + '\n']
    out, _ = vm.run(inp)
    return out[-1]


def solve(program):
    script = [
        'NOT A J',
        'NOT B T',
        'OR T J',
        'NOT C T',
        'OR T J',
        'AND D J',
        'NOT E T',
        'NOT T T',
        'OR H T',
        'AND T J',
        'RUN',
    ]
    return run_script(program, script)


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d21_input.txt').read_text().strip().split(',')]
    print(solve(p))
