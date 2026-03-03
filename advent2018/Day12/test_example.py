from day12 import load, solve
from day12_part2 import solve as solve_p2


def test_example_part1(tmp_path):
    sample = '''
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
'''.strip()
    p = tmp_path / 'in.txt'
    p.write_text(sample)
    s, r = load(p)
    assert solve(s, r) == 325


def test_part2_smoke(tmp_path):
    sample = '''
initial state: #..#.#..##......###...###

...## => #
..#.. => #
.#... => #
.#.#. => #
.#.## => #
.##.. => #
.#### => #
#.#.# => #
#.### => #
##.#. => #
##.## => #
###.. => #
###.# => #
####. => #
'''.strip()
    p = tmp_path / 'in.txt'
    p.write_text(sample)
    s, r = load(p)
    assert solve_p2(s, r, target=200) > 0


if __name__ == '__main__':
    from pathlib import Path
    t = Path('/tmp/day12_test')
    t.mkdir(exist_ok=True)
    class T:
        def __truediv__(self, o):
            return t / o
    test_example_part1(T())
    test_part2_smoke(T())
    print('ok')
