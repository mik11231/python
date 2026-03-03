"""Advent of Code 2019 Day 22 Part 1."""

from pathlib import Path


def solve(lines, n=10007, card=2019):
    pos = card
    for ln in lines:
        if ln.startswith('deal into new stack'):
            pos = n - 1 - pos
        elif ln.startswith('cut '):
            k = int(ln.split()[1])
            pos = (pos - k) % n
        else:
            k = int(ln.split()[-1])
            pos = (pos * k) % n
    return pos


if __name__ == '__main__':
    lines = [x.strip() for x in Path(__file__).with_name('d22_input.txt').read_text().splitlines() if x.strip()]
    print(solve(lines))
