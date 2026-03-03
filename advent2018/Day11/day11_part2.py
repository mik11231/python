from pathlib import Path


def power_level(x: int, y: int, serial: int) -> int:
    """Compute the fuel-cell power level at 1-indexed coordinate (x, y)."""
    rack_id = x + 10
    value = (rack_id * y + serial) * rack_id
    hundreds = (value // 100) % 10
    return hundreds - 5


def build_summed_area_table(serial: int) -> list[list[int]]:
    """Build SAT so any axis-aligned square sum is O(1).

    sat[x][y] stores the sum of cells in rectangle (1,1) to (x,y), inclusive.
    """
    sat = [[0] * 301 for _ in range(301)]
    for x in range(1, 301):
        row_acc = 0
        for y in range(1, 301):
            row_acc += power_level(x, y, serial)
            sat[x][y] = sat[x - 1][y] + row_acc
    return sat


def square_sum(sat: list[list[int]], x: int, y: int, size: int) -> int:
    """Return sum for square with top-left (x,y) and side length=size."""
    x2 = x + size - 1
    y2 = y + size - 1
    return sat[x2][y2] - sat[x - 1][y2] - sat[x2][y - 1] + sat[x - 1][y - 1]


def solve(serial: int) -> str:
    """Return 'x,y,size' for the highest-power square of any size."""
    sat = build_summed_area_table(serial)
    best_sum = None
    best_xyz = (0, 0, 0)

    for size in range(1, 301):
        limit = 301 - size
        for x in range(1, limit + 1):
            for y in range(1, limit + 1):
                total = square_sum(sat, x, y, size)
                if best_sum is None or total > best_sum:
                    best_sum = total
                    best_xyz = (x, y, size)

    x, y, size = best_xyz
    return f"{x},{y},{size}"


if __name__ == "__main__":
    serial = int(Path(__file__).with_name("d11_input.txt").read_text().strip())
    print(solve(serial))
