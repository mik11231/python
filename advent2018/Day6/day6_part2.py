"""Advent of Code 2018 solution module."""

from pathlib import Path


def load_points(path: Path) -> list[tuple[int, int]]:
    points = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        x_str, y_str = line.split(',')
        points.append((int(x_str.strip()), int(y_str.strip())))
    return points


def region_size(points: list[tuple[int, int]], distance_limit: int) -> int:
    min_x = min(x for x, _ in points)
    max_x = max(x for x, _ in points)
    min_y = min(y for _, y in points)
    max_y = max(y for _, y in points)

    count = 0
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            total = sum(abs(x - px) + abs(y - py) for px, py in points)
            if total < distance_limit:
                count += 1
    return count


def solve(points: list[tuple[int, int]], distance_limit: int = 10000) -> int:
    return region_size(points, distance_limit)


if __name__ == "__main__":
    input_path = Path(__file__).with_name("d6_input.txt")
    print(solve(load_points(input_path), distance_limit=10000))
