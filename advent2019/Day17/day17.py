"""Advent of Code 2019 Day 17 Part 1."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


def scaffold_map(program):
    """
    Run `scaffold_map` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    vm = IntcodeComputer(program)
    out, _ = vm.run([])
    s = ''.join(chr(c) for c in out)
    return [list(r) for r in s.strip().splitlines()]


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
    g = scaffold_map(program)
    h, w = len(g), len(g[0])
    ans = 0
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if g[y][x] == '#' and all(g[y + dy][x + dx] == '#' for dx, dy in [(0,-1),(0,1),(-1,0),(1,0)]):
                ans += x * y
    return ans


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d17_input.txt').read_text().strip().split(',')]
    print(solve(p))
