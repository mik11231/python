"""Advent of Code 2019 Day 22 Part 2."""

from pathlib import Path


def modinv(a, m):
    """
    Run `modinv` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: a, m.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    return pow(a, -1, m)


def solve(lines, m=119315717514047, reps=101741582076661, pos=2020):
    # Forward transform one shuffle: f(x)=a*x+b (x is original position).
    """
    Run `solve` as a clearly documented algorithm stage.
    
    Methodology:
    - Treat this function as one deterministic step in the Advent pipeline.
    - Keep parsing, state transitions, and result emission easy to audit.
    - Favor explicit control flow so behavior can be reasoned about from docs alone.
    
    Parameters: lines, m, reps, pos.
    - Produces side effects required by the caller (output/mutation/control flow).
    """
    a, b = 1, 0
    for ln in lines:
        if ln.startswith('deal into new stack'):
            a = (-a) % m
            b = (-b - 1) % m
        elif ln.startswith('cut '):
            k = int(ln.split()[1])
            b = (b - k) % m
        else:
            k = int(ln.split()[-1])
            a = (a * k) % m
            b = (b * k) % m

    ak = pow(a, reps, m)
    bk = (b * (ak - 1) * modinv((a - 1) % m, m)) % m if a != 1 else (b * reps) % m

    # Find card x that ends at target position pos: ak*x + bk = pos (mod m).
    x = ((pos - bk) * modinv(ak, m)) % m
    return x


if __name__ == '__main__':
    lines = [x.strip() for x in Path(__file__).with_name('d22_input.txt').read_text().splitlines() if x.strip()]
    print(solve(lines))
