"""Advent of Code 2019 Day 9 Part 2."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def solve(program: list[int]) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program.
    - Returns the computed result for this stage of the pipeline.
    """
    vm = IntcodeComputer(program)
    out, _ = vm.run([2])
    return out[-1]


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d9_input.txt').read_text().strip().split(',')]
    print(solve(p))
