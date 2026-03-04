"""Advent of Code 2019 Day 2 Part 2."""

from pathlib import Path


def run(mem: list[int]) -> list[int]:
    """
    Run `run` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: mem.
    - Returns the computed result for this stage of the pipeline.
    """
    ip = 0
    while True:
        op = mem[ip]
        if op == 99:
            return mem
        a, b, c = mem[ip + 1], mem[ip + 2], mem[ip + 3]
        if op == 1:
            mem[c] = mem[a] + mem[b]
        elif op == 2:
            mem[c] = mem[a] * mem[b]
        else:
            raise ValueError(op)
        ip += 4


def solve(program: list[int], target: int = 19690720) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: program, target.
    - Returns the computed result for this stage of the pipeline.
    """
    for noun in range(100):
        for verb in range(100):
            mem = program.copy()
            mem[1] = noun
            mem[2] = verb
            if run(mem)[0] == target:
                return 100 * noun + verb
    raise RuntimeError('not found')


if __name__ == '__main__':
    program = [int(x) for x in Path(__file__).with_name('d2_input.txt').read_text().strip().split(',')]
    print(solve(program))
