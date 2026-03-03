from day9 import play


def test_examples():
    assert play(9, 25) == 32
    assert play(10, 1618) == 8317
    assert play(13, 7999) == 146373


if __name__ == "__main__":
    test_examples()
    print("ok")
