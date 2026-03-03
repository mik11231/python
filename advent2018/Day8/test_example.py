from day8 import solve as solve_part1
from day8_part2 import solve as solve_part2


def test_part1():
    assert solve_part1([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]) == 138


def test_part2():
    assert solve_part2([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]) == 66


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("ok")
