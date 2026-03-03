from pathlib import Path


def load_constants(path: Path):
    """Extract key constants from input program lines used in the hot loop."""
    lines = [line.strip().split() for line in path.read_text().splitlines() if line.strip()]
    # Program structure is fixed for AoC 2018 Day 21; these literals define the loop.
    or_mask = int(lines[7][2])   # bori r1 <mask> r2
    seed = int(lines[8][1])      # seti <seed> ... -> r1
    byte_mask = int(lines[9][2])
    full_mask = int(lines[11][2])
    mul_const = int(lines[12][2])
    return seed, or_mask, byte_mask, full_mask, mul_const


def next_value(r1: int, seed: int, or_mask: int, byte_mask: int, full_mask: int, mul_const: int) -> int:
    """Compute one value that will be compared against r0 at instruction 28."""
    r2 = r1 | or_mask
    r1 = seed

    while True:
        r1 = (r1 + (r2 & byte_mask)) & full_mask
        r1 = (r1 * mul_const) & full_mask
        if r2 < 256:
            return r1
        r2 //= 256


def solve(path: Path) -> int:
    seed, or_mask, byte_mask, full_mask, mul_const = load_constants(path)
    return next_value(0, seed, or_mask, byte_mask, full_mask, mul_const)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d21_input.txt')))
