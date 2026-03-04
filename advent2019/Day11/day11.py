"""Advent of Code 2019 Day 11 Part 1."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def paint(program, start_color=0):
    """
    Run `paint` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program, start_color.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    vm = IntcodeComputer(program)
    grid = {(0, 0): start_color}
    painted = set()
    x = y = 0
    d = 0

    while not vm.halted:
        cur = grid.get((x, y), 0)
        out1, _ = vm.run([cur], stop_on_output=True)
        if vm.halted:
            break
        out2, _ = vm.run([], stop_on_output=True)
        if not out1 or not out2:
            break
        color = out1[-1]
        turn = out2[-1]

        grid[(x, y)] = color
        painted.add((x, y))

        d = (d - 1) % 4 if turn == 0 else (d + 1) % 4
        dx, dy = DIRS[d]
        x += dx
        y += dy

    return grid, painted


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
    _, painted = paint(program, 0)
    return len(painted)


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d11_input.txt').read_text().strip().split(',')]
    print(solve(p))
