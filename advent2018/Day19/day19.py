"""Advent of Code 2018 solution module."""

from pathlib import Path


def apply(op, a, b, c, r):
    """
    Run `apply` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: op, a, b, c, r.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    if op == 'addr': r[c] = r[a] + r[b]
    elif op == 'addi': r[c] = r[a] + b
    elif op == 'mulr': r[c] = r[a] * r[b]
    elif op == 'muli': r[c] = r[a] * b
    elif op == 'banr': r[c] = r[a] & r[b]
    elif op == 'bani': r[c] = r[a] & b
    elif op == 'borr': r[c] = r[a] | r[b]
    elif op == 'bori': r[c] = r[a] | b
    elif op == 'setr': r[c] = r[a]
    elif op == 'seti': r[c] = a
    elif op == 'gtir': r[c] = 1 if a > r[b] else 0
    elif op == 'gtri': r[c] = 1 if r[a] > b else 0
    elif op == 'gtrr': r[c] = 1 if r[a] > r[b] else 0
    elif op == 'eqir': r[c] = 1 if a == r[b] else 0
    elif op == 'eqri': r[c] = 1 if r[a] == b else 0
    elif op == 'eqrr': r[c] = 1 if r[a] == r[b] else 0
    else: raise ValueError(op)


def load(path: Path):
    """
    Run `load` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    ip_reg = int(lines[0].split()[1])
    prog = []
    for line in lines[1:]:
        op, a, b, c = line.split()
        prog.append((op, int(a), int(b), int(c)))
    return ip_reg, prog


def run(ip_reg, prog, r0=0, max_steps=50_000_000):
    """
    Run `run` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: ip_reg, prog, r0, max_steps.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    r = [0, 0, 0, 0, 0, 0]
    r[0] = r0
    ip = 0
    steps = 0
    while 0 <= ip < len(prog):
        r[ip_reg] = ip
        op, a, b, c = prog[ip]
        apply(op, a, b, c, r)
        ip = r[ip_reg] + 1
        steps += 1
        if steps >= max_steps:
            raise RuntimeError('step limit reached')
    return r


def solve(path: Path) -> int:
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Returns the computed result for this stage of the pipeline.
    """
    ip_reg, prog = load(path)
    r = run(ip_reg, prog, r0=0)
    return r[0]


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d19_input.txt')))
