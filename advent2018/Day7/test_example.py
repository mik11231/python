from day7 import solve as solve_part1
from day7_part2 import solve as solve_part2


EXAMPLE = [
    ("C", "A"),
    ("C", "F"),
    ("A", "B"),
    ("A", "D"),
    ("B", "E"),
    ("D", "E"),
    ("F", "E"),
]


def test_part1():
    assert solve_part1(EXAMPLE) == "CABDFE"


def test_part2():
    assert solve_part2(EXAMPLE, workers=2, base=0) == 15


if __name__ == "__main__":
    test_part1()
    test_part2()
    print("ok")
