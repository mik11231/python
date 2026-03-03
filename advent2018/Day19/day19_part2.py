from pathlib import Path


def apply(op, a, b, c, r):
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
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    ip_reg = int(lines[0].split()[1])
    prog = []
    for line in lines[1:]:
        op, a, b, c = line.split()
        prog.append((op, int(a), int(b), int(c)))
    return ip_reg, prog


def extract_target(ip_reg, prog):
    """Run only initialization for r0=1 and read divisor target from register 4."""
    r = [1, 0, 0, 0, 0, 0]
    ip = 0

    # Program enters divisor loop at ip=1; stop once reached.
    while ip != 1:
        r[ip_reg] = ip
        op, a, b, c = prog[ip]
        apply(op, a, b, c, r)
        ip = r[ip_reg] + 1
    return r[4]


def sum_divisors(n: int) -> int:
    total = 0
    d = 1
    while d * d <= n:
        if n % d == 0:
            total += d
            if d * d != n:
                total += n // d
        d += 1
    return total


def solve(path: Path) -> int:
    ip_reg, prog = load(path)
    target = extract_target(ip_reg, prog)
    return sum_divisors(target)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d19_input.txt')))
