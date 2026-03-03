from pathlib import Path


def load(path: Path) -> tuple[set[int], set[str]]:
    """Parse initial plant positions and rules that produce a plant (#)."""
    lines = [line.strip() for line in path.read_text().splitlines() if line.strip()]
    initial = lines[0].split(': ')[1]
    state = {i for i, ch in enumerate(initial) if ch == '#'}
    rules = {line.split(' => ')[0] for line in lines[1:] if line.endswith('=> #')}
    return state, rules


def next_state(state: set[int], rules: set[str]) -> set[int]:
    """Advance one generation using 5-char neighborhood rules."""
    if not state:
        return set()
    lo, hi = min(state) - 2, max(state) + 2
    out = set()
    for i in range(lo, hi + 1):
        pattern = ''.join('#' if j in state else '.' for j in range(i - 2, i + 3))
        if pattern in rules:
            out.add(i)
    return out


def simulate(state: set[int], rules: set[str], generations: int) -> int:
    """Run fixed-number simulation and return sum of live pot indices."""
    for _ in range(generations):
        state = next_state(state, rules)
    return sum(state)


def solve(state: set[int], rules: set[str]) -> int:
    return simulate(state, rules, 20)


if __name__ == '__main__':
    s, r = load(Path(__file__).with_name('d12_input.txt'))
    print(solve(s, r))
