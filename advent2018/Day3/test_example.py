from day3 import solve as solve_part1
from day3_part2 import solve as solve_part2


def test_part1_example():
    claims = [
        (1, 1, 3, 4, 4),
        (2, 3, 1, 4, 4),
        (3, 5, 5, 2, 2),
    ]
    assert solve_part1(claims) == 4


def test_part2_example():
    claims = [
        (1, 1, 3, 4, 4),
        (2, 3, 1, 4, 4),
        (3, 5, 5, 2, 2),
    ]
    assert solve_part2(claims) == 3

if __name__ == "__main__":
    test_part1_example()
    test_part2_example()
    print("ok")
