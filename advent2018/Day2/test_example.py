from day2 import solve as solve_part1
from day2_part2 import solve as solve_part2


def test_part1_example():
    ids = [
        "abcdef",
        "bababc",
        "abbcde",
        "abcccd",
        "aabcdd",
        "abcdee",
        "ababab",
    ]
    assert solve_part1(ids) == 12


def test_part2_example():
    ids = ["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"]
    assert solve_part2(ids) == "fgij"

if __name__ == "__main__":
    test_part1_example()
    test_part2_example()
    print("ok")
