"""Advent of Code 2019 Day 12 Part 1."""

import re
from pathlib import Path


def load(s):
    """
    Run `load` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return [list(map(int, re.findall(r'-?\d+', line))) for line in s.splitlines() if line.strip()]


def step(pos, vel):
    """
    Run `step` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: pos, vel.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    n = len(pos)
    for i in range(n):
        for j in range(i + 1, n):
            for a in range(3):
                if pos[i][a] < pos[j][a]:
                    vel[i][a] += 1; vel[j][a] -= 1
                elif pos[i][a] > pos[j][a]:
                    vel[i][a] -= 1; vel[j][a] += 1
    for i in range(n):
        for a in range(3):
            pos[i][a] += vel[i][a]


def solve(s: str, steps=1000) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: s, steps.
    - Returns the computed result for this stage of the pipeline.
    """
    pos = load(s)
    vel = [[0, 0, 0] for _ in pos]
    for _ in range(steps):
        step(pos, vel)
    return sum(sum(abs(v) for v in p) * sum(abs(v) for v in q) for p, q in zip(pos, vel))


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d12_input.txt').read_text(), 1000))
