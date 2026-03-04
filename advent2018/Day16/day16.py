"""Advent of Code 2018 solution module."""

import re
from pathlib import Path


def apply(op: str, a: int, b: int, c: int, r: list[int]) -> list[int]:
    """Execute one opcode variant and return a new register list."""
    out = r.copy()
    if op == 'addr': out[c] = r[a] + r[b]
    elif op == 'addi': out[c] = r[a] + b
    elif op == 'mulr': out[c] = r[a] * r[b]
    elif op == 'muli': out[c] = r[a] * b
    elif op == 'banr': out[c] = r[a] & r[b]
    elif op == 'bani': out[c] = r[a] & b
    elif op == 'borr': out[c] = r[a] | r[b]
    elif op == 'bori': out[c] = r[a] | b
    elif op == 'setr': out[c] = r[a]
    elif op == 'seti': out[c] = a
    elif op == 'gtir': out[c] = 1 if a > r[b] else 0
    elif op == 'gtri': out[c] = 1 if r[a] > b else 0
    elif op == 'gtrr': out[c] = 1 if r[a] > r[b] else 0
    elif op == 'eqir': out[c] = 1 if a == r[b] else 0
    elif op == 'eqri': out[c] = 1 if r[a] == b else 0
    elif op == 'eqrr': out[c] = 1 if r[a] == r[b] else 0
    else: raise ValueError(op)
    return out


OPS = {
    'addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
    'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr'
}


def parse(path: Path):
    """
    Run `parse` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: path.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    text = path.read_text().rstrip('\n')
    parts = text.split('\n\n\n\n')
    sample_block, prog_block = parts[0], parts[1]

    samples = []
    lines = sample_block.splitlines()
    i = 0
    while i < len(lines):
        if not lines[i].startswith('Before:'):
            i += 1
            continue
        before = list(map(int, re.findall(r'\d+', lines[i])))
        instr = list(map(int, lines[i + 1].split()))
        after = list(map(int, re.findall(r'\d+', lines[i + 2])))
        samples.append((before, instr, after))
        i += 4

    program = [tuple(map(int, line.split())) for line in prog_block.splitlines() if line.strip()]
    return samples, program


def solve(samples) -> int:
    """Count samples behaving like 3+ opcodes (part 1)."""
    cnt = 0
    for before, (_, a, b, c), after in samples:
        matches = 0
        for op in OPS:
            if apply(op, a, b, c, before) == after:
                matches += 1
        if matches >= 3:
            cnt += 1
    return cnt


if __name__ == '__main__':
    s, _ = parse(Path(__file__).with_name('d16_input.txt'))
    print(solve(s))
