"""Advent of Code 2018 solution module."""

from pathlib import Path


def load_clay(path: Path):
    """Parse clay scan lines into a coordinate set and y-bounds."""
    clay = set()
    min_y = 10**9
    max_y = -10**9

    for line in path.read_text().splitlines():
        a, b = line.split(', ')
        if a.startswith('x='):
            x = int(a[2:])
            y1, y2 = map(int, b[2:].split('..'))
            for y in range(y1, y2 + 1):
                clay.add((x, y))
            min_y = min(min_y, y1)
            max_y = max(max_y, y2)
        else:
            y = int(a[2:])
            x1, x2 = map(int, b[2:].split('..'))
            for x in range(x1, x2 + 1):
                clay.add((x, y))
            min_y = min(min_y, y)
            max_y = max(max_y, y)

    return clay, min_y, max_y


def simulate(clay: set[tuple[int, int]], min_y: int, max_y: int):
    """Iteratively simulate flowing (~) and settled (|) water from spring x=500."""
    flowing = set()
    settled = set()

    def blocked(x: int, y: int) -> bool:
        return (x, y) in clay or (x, y) in settled

    stack = [(500, min_y)]
    processed_sources = set()

    while stack:
        x, y = stack.pop()
        if (x, y) in processed_sources:
            continue
        processed_sources.add((x, y))

        # Fall vertically until we hit support or leave scan range.
        while y <= max_y and not blocked(x, y):
            flowing.add((x, y))
            y += 1

        if y > max_y:
            continue

        # We stopped because y is blocked; process lateral spreading at y-1.
        y -= 1

        while True:
            # Scan left while floor support exists.
            lx = x
            left_open = False
            while True:
                if not blocked(lx, y + 1):
                    left_open = True
                    break
                if (lx - 1, y) in clay:
                    break
                lx -= 1

            # Scan right while floor support exists.
            rx = x
            right_open = False
            while True:
                if not blocked(rx, y + 1):
                    right_open = True
                    break
                if (rx + 1, y) in clay:
                    break
                rx += 1

            for xx in range(lx, rx + 1):
                flowing.add((xx, y))

            if not left_open and not right_open:
                # Basin row: convert to settled, then move one row up.
                for xx in range(lx, rx + 1):
                    settled.add((xx, y))
                y -= 1
                if y < min_y:
                    break
                continue

            # Spill edges become new vertical sources.
            if left_open:
                src = (lx, y)
                if src not in processed_sources:
                    stack.append(src)
            if right_open:
                src = (rx, y)
                if src not in processed_sources:
                    stack.append(src)
            break

    return flowing, settled


def solve(path: Path) -> int:
    clay, min_y, max_y = load_clay(path)
    flowing, settled = simulate(clay, min_y, max_y)
    all_water = flowing | settled
    return sum(1 for _, y in all_water if min_y <= y <= max_y)


if __name__ == '__main__':
    print(solve(Path(__file__).with_name('d17_input.txt')))
