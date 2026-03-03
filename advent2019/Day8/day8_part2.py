"""Advent of Code 2019 Day 8 Part 2."""

from pathlib import Path


def solve(data: str, w: int = 25, h: int = 6) -> str:
    size = w * h
    layers = [data[i:i + size] for i in range(0, len(data), size)]
    out = ['2'] * size
    for i in range(size):
        for lay in layers:
            if lay[i] != '2':
                out[i] = lay[i]
                break

    rows = []
    for y in range(h):
        row = ''.join('##' if c == '1' else '  ' for c in out[y * w:(y + 1) * w])
        rows.append(row)
    return '\n'.join(rows)


if __name__ == '__main__':
    s = Path(__file__).with_name('d8_input.txt').read_text().strip()
    print(solve(s))
