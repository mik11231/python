"""Advent of Code 2019 Day 23 Part 2."""

from collections import deque
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


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
    vms = [IntcodeComputer(program) for _ in range(50)]
    q = [deque([i]) for i in range(50)]

    nat = None
    seen_y = set()

    while True:
        network_idle = True

        for i in range(50):
            if q[i]:
                inp = list(q[i])
                q[i].clear()
                network_idle = False
            else:
                inp = [-1]
            out, _ = vms[i].run(inp)
            if out:
                network_idle = False
            for j in range(0, len(out), 3):
                a, x, y = out[j:j+3]
                if a == 255:
                    nat = (x, y)
                else:
                    q[a].append(x)
                    q[a].append(y)

        if network_idle and all(len(qq) == 0 for qq in q) and nat is not None:
            x, y = nat
            q[0].append(x)
            q[0].append(y)
            if y in seen_y:
                return y
            seen_y.add(y)


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d23_input.txt').read_text().strip().split(',')]
    print(solve(p))
