from day1 import solve as solve_part1
from day1_part2 import solve as solve_part2


def test_part1_example():
    assert solve_part1([1, -2, 3, 1]) == 3


def test_part2_example():
    assert solve_part2([1, -2, 3, 1]) == 2

if __name__ == "__main__":
    test_part1_example()
    test_part2_example()
    print("ok")
