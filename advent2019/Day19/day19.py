"""Advent of Code 2019 Day 19 Part 1."""

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
    return sum(probe(program, x, y) for y in range(50) for x in range(50))


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d19_input.txt').read_text().strip().split(',')]
    print(solve(p))
