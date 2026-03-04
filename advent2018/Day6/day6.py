"""Advent of Code 2018 solution module."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from aoclib.geometry import manhattan2


def load_points(path: Path) -> list[tuple[int, int]]:
    points = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        x_str, y_str = line.split(',')
        points.append((int(x_str.strip()), int(y_str.strip())))
    return points


def largest_finite_area(points: list[tuple[int, int]]) -> int:
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)

    area = [0] * len(points)
    infinite = set()

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            here = (x, y)
            dists = [manhattan2(here, (px, py)) for px, py in points]
            best = min(dists)
            if dists.count(best) > 1:
                continue
            idx = dists.index(best)
            area[idx] += 1
            if x in (min_x, max_x) or y in (min_y, max_y):
                infinite.add(idx)

    return max(area[i] for i in range(len(points)) if i not in infinite)


def solve(points: list[tuple[int, int]]) -> int:
    return largest_finite_area(points)


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d6_input.txt")
    print(solve(load_points(input_path)))
