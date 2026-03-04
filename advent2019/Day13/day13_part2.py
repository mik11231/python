"""Advent of Code 2019 Day 13 Part 2."""

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
    mem = program.copy()
    mem[0] = 2
    vm = IntcodeComputer(mem)

    score = 0
    paddle_x = 0
    ball_x = 0
    joystick = 0

    while not vm.halted:
        outputs, _ = vm.run([joystick])
        for i in range(0, len(outputs), 3):
            x, y, t = outputs[i:i + 3]
            if x == -1 and y == 0:
                score = t
            else:
                if t == 3:
                    paddle_x = x
                elif t == 4:
                    ball_x = x
        joystick = (ball_x > paddle_x) - (ball_x < paddle_x)

    return score


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d13_input.txt').read_text().strip().split(',')]
    print(solve(p))
