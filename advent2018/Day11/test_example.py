from day11 import power_level, solve as solve_part1
from day11_part2 import solve as solve_part2


def test_power_level_examples():
    assert power_level(3, 5, 8) == 4
    assert power_level(122, 79, 57) == -5
    assert power_level(217, 196, 39) == 0
    assert power_level(101, 153, 71) == 4


def test_part1_examples():
    assert solve_part1(18) == "33,45"
    assert solve_part1(42) == "21,61"


def test_part2_examples():
    assert solve_part2(18) == "90,269,16"
    assert solve_part2(42) == "232,251,12"


if __name__ == "__main__":
    test_power_level_examples()
    test_part1_examples()
    test_part2_examples()
    print("ok")
