#!/usr/bin/env python3
"""Tests for Day 25 using the example from the problem statement.

Card public key: 5764801 (loop size 8)
Door public key: 17807724 (loop size 11)
Encryption key:  14897079
"""

from day25 import find_loop_size, transform, find_encryption_key

CARD_PUBLIC = 5764801
DOOR_PUBLIC = 17807724


def test_loop_sizes():
    """Verify card loop size is 8 and door loop size is 11."""
    assert find_loop_size(CARD_PUBLIC) == 8
    assert find_loop_size(DOOR_PUBLIC) == 11
    print("PASS  loop sizes: card=8, door=11")


def test_encryption_key_via_card():
    """Verify encryption key 14897079 when derived via card loop size."""
    key = transform(DOOR_PUBLIC, find_loop_size(CARD_PUBLIC))
    assert key == 14897079, f"Expected 14897079, got {key}"
    print(f"PASS  encryption key (via card loop): {key}")


def test_encryption_key_via_door():
    """Verify encryption key 14897079 when derived via door loop size."""
    key = transform(CARD_PUBLIC, find_loop_size(DOOR_PUBLIC))
    assert key == 14897079, f"Expected 14897079, got {key}"
    print(f"PASS  encryption key (via door loop): {key}")


def test_find_encryption_key():
    """Verify Part 1: find_encryption_key returns 14897079."""
    key = find_encryption_key(CARD_PUBLIC, DOOR_PUBLIC)
    assert key == 14897079, f"Expected 14897079, got {key}"
    print(f"PASS  Part 1: encryption key = {key}")


if __name__ == "__main__":
    test_loop_sizes()
    test_encryption_key_via_card()
    test_encryption_key_via_door()
    test_find_encryption_key()
    print("\nAll Day 25 tests passed!")
