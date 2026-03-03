from day5 import react, solve as solve_part1
from day5_part2 import solve as solve_part2


EXAMPLE = "dabAcCaCBAcCcaDA"


def test_reaction_example():
    assert react(EXAMPLE) == "dabCBAcaDA"


def test_part1_example():
    assert solve_part1(EXAMPLE) == 10


def test_part2_example():
    assert solve_part2(EXAMPLE) == 4


if __name__ == "__main__":
    test_reaction_example()
    test_part1_example()
    test_part2_example()
    print("ok")
