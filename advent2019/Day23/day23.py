"""Advent of Code 2019 Day 23 Part 1."""

from collections import deque
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def solve(program):
    vms = [IntcodeComputer(program) for _ in range(50)]
    q = [deque([i]) for i in range(50)]

    while True:
        for i in range(50):
            if q[i]:
                inp = list(q[i])
                q[i].clear()
            else:
                inp = [-1]
            out, _ = vms[i].run(inp)
            for j in range(0, len(out), 3):
                a, x, y = out[j:j+3]
                if a == 255:
                    return y
                q[a].append(x)
                q[a].append(y)


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d23_input.txt').read_text().strip().split(',')]
    print(solve(p))
