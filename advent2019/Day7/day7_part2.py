"""Advent of Code 2019 Day 7 Part 2."""

from itertools import permutations
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def solve(program: list[int]) -> int:
    best = 0
    for perm in permutations([5, 6, 7, 8, 9]):
        vms = [IntcodeComputer(program) for _ in range(5)]
        for vm, phase in zip(vms, perm):
            vm.run([phase])

        sig = 0
        last = 0
        i = 0
        while not vms[-1].halted:
            out, _ = vms[i].run([sig], stop_on_output=True)
            if out:
                sig = out[-1]
                if i == 4:
                    last = sig
            i = (i + 1) % 5
        best = max(best, last)
    return best


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d7_input.txt').read_text().strip().split(',')]
    print(solve(p))
