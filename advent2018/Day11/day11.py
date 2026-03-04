"""Advent of Code 2018 solution module."""

from pathlib import Path


def power_level(x: int, y: int, serial: int) -> int:
    """Compute the fuel-cell power level at 1-indexed coordinate (x, y)."""
    rack_id = x + 10
    value = (rack_id * y + serial) * rack_id
    hundreds = (value // 100) % 10
    return hundreds - 5


def solve(serial: int) -> str:
    """Return the top-left coordinate of the best 3x3 square as 'x,y'."""
    best_sum = None
    best_xy = (0, 0)

    # Only top-left positions that allow a full 3x3 window are valid.
    for x in range(1, 299):
        for y in range(1, 299):
            square_sum = 0
            for dx in range(3):
                for dy in range(3):
                    square_sum += power_level(x + dx, y + dy, serial)
            if best_sum is None or square_sum > best_sum:
                best_sum = square_sum
                best_xy = (x, y)

    return f"{best_xy[0]},{best_xy[1]}"


if __name__ == "__main__":
    serial = int(Path(__file__).with_name("d11_input.txt").read_text().strip())
    print(solve(serial))
