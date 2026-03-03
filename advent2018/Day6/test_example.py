from day6 import solve as solve_part1
from day6_part2 import solve as solve_part2


EXAMPLE_POINTS = [
    (1, 1),
    (1, 6),
    (8, 3),
    (3, 4),
    (5, 5),
    (8, 9),
]


def test_part1_example():
    assert solve_part1(EXAMPLE_POINTS) == 17


def test_part2_example():
    assert solve_part2(EXAMPLE_POINTS, distance_limit=32) == 16


if __name__ == "__main__":
    test_part1_example()
    test_part2_example()
    print("ok")
