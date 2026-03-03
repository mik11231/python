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


def solve(state: set[int], rules: set[str], target: int = 50_000_000_000) -> int:
    """Detect linear growth of sum(state) and extrapolate to target generation."""
    prev_sum = sum(state)
    prev_delta = None
    stable_count = 0

    for gen in range(1, target + 1):
        state = next_state(state, rules)
        cur_sum = sum(state)
        delta = cur_sum - prev_sum

        # Once the shape drifts by a fixed offset each generation, delta stabilizes.
        if delta == prev_delta:
            stable_count += 1
            if stable_count >= 100:
                remaining = target - gen
                return cur_sum + remaining * delta
        else:
            stable_count = 0

        prev_delta = delta
        prev_sum = cur_sum

    return prev_sum


if __name__ == '__main__':
    s, r = load(Path(__file__).with_name('d12_input.txt'))
    print(solve(s, r))
