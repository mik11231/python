from day14 import solve as solve_part1
from day14_part2 import solve as solve_part2


def test_part1_examples():
    assert solve_part1(9) == '5158916779'
    assert solve_part1(5) == '0124515891'
    assert solve_part1(18) == '9251071085'
    assert solve_part1(2018) == '5941429882'


def test_part2_examples():
    assert solve_part2('51589') == 9
    assert solve_part2('01245') == 5
    assert solve_part2('92510') == 18
    assert solve_part2('59414') == 2018


if __name__ == '__main__':
    test_part1_examples()
    test_part2_examples()
    print('ok')
