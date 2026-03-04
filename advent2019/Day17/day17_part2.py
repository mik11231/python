"""Advent of Code 2019 Day 17 Part 2."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from advent2019.intcode import IntcodeComputer


DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
LEFT = lambda d: (d - 1) % 4
RIGHT = lambda d: (d + 1) % 4
ROBOT = {'^': 0, '>': 1, 'v': 2, '<': 3}


def get_grid(program):
    """
    Run `get_grid` as a clearly documented algorithm stage.
    
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
    g = [list(r) for r in s.strip().splitlines()]
    return g


def inb(g, x, y):
    """
    Run `inb` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: g, x, y.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return 0 <= y < len(g) and 0 <= x < len(g[0])


def path_tokens(g):
    # Find robot start + direction.
    """
    Run `path_tokens` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: g.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    for y, row in enumerate(g):
        for x, ch in enumerate(row):
            if ch in ROBOT:
                d = ROBOT[ch]
                sx, sy = x, y
                break

    x, y = sx, sy
    tokens = []

    while True:
        # Try turn left or right to find next scaffold direction.
        turned = None
        for turn, nd in [('L', LEFT(d)), ('R', RIGHT(d))]:
            dx, dy = DIRS[nd]
            nx, ny = x + dx, y + dy
            if inb(g, nx, ny) and g[ny][nx] == '#':
                turned = (turn, nd)
                break
        if turned is None:
            break
        turn, d = turned
        tokens.append(turn)

        steps = 0
        dx, dy = DIRS[d]
        while True:
            nx, ny = x + dx, y + dy
            if not inb(g, nx, ny) or g[ny][nx] != '#':
                break
            x, y = nx, ny
            steps += 1
        tokens.append(str(steps))

    return tokens


def enc(tokens):
    """
    Run `enc` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: tokens.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return ','.join(tokens)


def fits(tokens):
    """
    Run `fits` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: tokens.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return len(enc(tokens)) <= 20


def compress(tokens):
    """
    Run `compress` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: tokens.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    n = len(tokens)
    for a_end in range(2, min(11, n + 1), 2):
        A = tokens[:a_end]
        if not fits(A):
            continue

        def replace(seq, pat, sym):
            """
            Run `replace` as a clearly documented algorithm stage.
            
            Methodology:
            - Treat this function as one deterministic step in the Advent pipeline.
            - Keep parsing, state transitions, and result emission easy to audit.
            - Favor explicit control flow so behavior can be reasoned about from docs alone.
            
            Parameters: seq, pat, sym.
            - Produces side effects required by the caller (output/mutation/control flow).
            """
            out = []
            i = 0
            while i < len(seq):
                if seq[i:i+len(pat)] == pat:
                    out.append(sym)
                    i += len(pat)
                else:
                    out.append(seq[i])
                    i += 1
            return out

        rA = replace(tokens, A, 'A')
        iB = next((i for i,t in enumerate(rA) if t not in {'A','B','C'}), None)
        if iB is None:
            continue
        for b_len in range(2, min(11, n - iB + 1), 2):
            B = rA[iB:iB+b_len]
            if any(x in {'A','B','C'} for x in B) or not fits(B):
                continue
            rB = replace(rA, B, 'B')
            iC = next((i for i,t in enumerate(rB) if t not in {'A','B','C'}), None)
            if iC is None:
                main = rB
                if fits(main):
                    return main, A, B, []
                continue
            for c_len in range(2, min(11, n - iC + 1), 2):
                C = rB[iC:iC+c_len]
                if any(x in {'A','B','C'} for x in C) or not fits(C):
                    continue
                rC = replace(rB, C, 'C')
                if all(t in {'A','B','C'} for t in rC) and fits(rC):
                    return rC, A, B, C
    raise RuntimeError('no compression')


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
    g = get_grid(program)
    tokens = path_tokens(g)
    main, A, B, C = compress(tokens)

    mem = program.copy()
    mem[0] = 2
    vm = IntcodeComputer(mem)

    script = '\n'.join([
        enc(main),
        enc(A),
        enc(B),
        enc(C),
        'n',
        ''
    ])
    inputs = [ord(c) for c in script]
    out, _ = vm.run(inputs)
    return out[-1]


if __name__ == '__main__':
    p = [int(x) for x in Path(__file__).with_name('d17_input.txt').read_text().strip().split(',')]
    print(solve(p))
