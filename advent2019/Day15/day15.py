"""Advent of Code 2019 Day 15 Part 1."""

from collections import deque
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


DIRS = {
    1: (0, -1),  # north
    2: (0, 1),   # south
    3: (-1, 0),  # west
    4: (1, 0),   # east
}
REV = {1: 2, 2: 1, 3: 4, 4: 3}


def step(vm: IntcodeComputer, cmd: int) -> int:
    """
    Run `step` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: vm, cmd.
    - Returns the computed result for this stage of the pipeline.
    """
    out, _ = vm.run([cmd], stop_on_output=True)
    return out[-1]


def explore(program):
    """
    Run `explore` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    vm = IntcodeComputer(program)
    grid = {(0, 0): 1}
    oxygen = None

    def dfs(x, y):
        """
        Run `dfs` as a clearly documented algorithm stage.
        
        Methodology:
        - Treat this function as one deterministic step in the Advent pipeline.
        - Keep parsing, state transitions, and result emission easy to audit.
        - Favor explicit control flow so behavior can be reasoned about from docs alone.
        
        Parameters: x, y.
        - Produces side effects required by the caller (output/mutation/control flow).
        """
        nonlocal oxygen
        for cmd, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if (nx, ny) in grid:
                continue
            status = step(vm, cmd)
            if status == 0:
                grid[(nx, ny)] = 0
                continue
            grid[(nx, ny)] = 1 if status == 1 else 2
            if status == 2:
                oxygen = (nx, ny)
            dfs(nx, ny)
            step(vm, REV[cmd])

    dfs(0, 0)
    return grid, oxygen


def shortest(grid, src, dst):
    """
    Run `shortest` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: grid, src, dst.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    q = deque([(src, 0)])
    seen = {src}
    while q:
        p, d = q.popleft()
        if p == dst:
            return d
        x, y = p
        for dx, dy in DIRS.values():
            np = (x + dx, y + dy)
            if np in seen:
                continue
            if grid.get(np, 0) == 0:
                continue
            seen.add(np)
            q.append((np, d + 1))
    raise RuntimeError('no path')


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
    grid, oxy = explore(program)
    return shortest(grid, (0, 0), oxy)


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d15_input.txt').read_text().strip().split(',')]
    print(solve(p))
