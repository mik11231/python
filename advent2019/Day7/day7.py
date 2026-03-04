"""Advent of Code 2019 Day 7 Part 1."""

from itertools import permutations
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def run_amp(program, phase, signal):
    """
    Run `run_amp` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program, phase, signal.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    vm = IntcodeComputer(program)
    out, _ = vm.run([phase, signal])
    return out[-1]


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
    best = 0
    for perm in permutations([0, 1, 2, 3, 4]):
        sig = 0
        for p in perm:
            sig = run_amp(program, p, sig)
        best = max(best, sig)
    return best


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d7_input.txt').read_text().strip().split(',')]
    print(solve(p))
