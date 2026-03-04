"""Advent of Code 2019 Day 19 Part 2."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def probe(program, x, y):
    """
    Run `probe` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program, x, y.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    vm = IntcodeComputer(program)
    out, _ = vm.run([x, y])
    return out[-1]


def solve(program):
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
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
