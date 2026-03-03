"""Advent of Code 2019 Day 8 Part 1."""

from pathlib import Path


def solve(data: str, w: int = 25, h: int = 6) -> int:
    size = w * h
    layers = [data[i:i + size] for i in range(0, len(data), size)]
    best = min(layers, key=lambda x: x.count('0'))
    return best.count('1') * best.count('2')


if __name__ == '__main__':
    s = Path(__file__).with_name('d8_input.txt').read_text().strip()
    print(solve(s))
