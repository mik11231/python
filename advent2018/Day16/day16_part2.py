from pathlib import Path
from day16 import OPS, apply, parse


def deduce_mapping(samples):
    """Use sample constraints + elimination to map numeric opcode -> real opcode."""
    possible = {i: set(OPS) for i in range(16)}

    for before, (code, a, b, c), after in samples:
        valid = {op for op in OPS if apply(op, a, b, c, before) == after}
        possible[code] &= valid

    mapping = {}
    while len(mapping) < 16:
        progress = False
        for code in range(16):
            if code in mapping:
                continue
            if len(possible[code]) == 1:
                op = next(iter(possible[code]))
                mapping[code] = op
                for other in range(16):
                    if other != code:
                        possible[other].discard(op)
                progress = True
        if not progress:
            raise RuntimeError('Could not fully resolve opcode mapping')

    return mapping


def solve(samples, program) -> int:
    mapping = deduce_mapping(samples)
    regs = [0, 0, 0, 0]
    for code, a, b, c in program:
        regs = apply(mapping[code], a, b, c, regs)
    return regs[0]


if __name__ == '__main__':
    s, p = parse(Path(__file__).with_name('d16_input.txt'))
    print(solve(s, p))
