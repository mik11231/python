from pathlib import Path


def recipes_after(n: int) -> str:
    """Return the 10-score sequence immediately after recipe index n."""
    board = [3, 7]
    a, b = 0, 1
    while len(board) < n + 10:
        s = board[a] + board[b]
        if s >= 10:
            board.append(1)
        board.append(s % 10)
        a = (a + 1 + board[a]) % len(board)
        b = (b + 1 + board[b]) % len(board)
    return ''.join(str(x) for x in board[n:n + 10])


def solve(n: int) -> str:
    return recipes_after(n)


if __name__ == '__main__':
    n = int(Path(__file__).with_name('d14_input.txt').read_text().strip())
    print(solve(n))
