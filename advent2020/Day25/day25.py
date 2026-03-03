#!/usr/bin/env python3
"""
Advent of Code 2020 - Day 25: Combo Breaker (Part 1)

Two devices (card and door) each have a public key derived from a secret
loop size.  To transform a subject number, start with value=1 and repeatedly
compute ``value = (value * subject_number) % 20201227``.  The public key is
the result of transforming subject number 7 by the device's secret loop size.

Given the two public keys, find one device's loop size, then compute the
encryption key by transforming the *other* device's public key by that loop
size.

Algorithm
---------
Brute-force the discrete-log problem: iterate the transform with subject 7
until the value equals a public key, counting iterations.  Then perform the
same transform with the other public key as the subject for that many steps.
The modulus (20201227) is small enough that this completes quickly.
"""

from pathlib import Path

MODULO = 20201227


def find_loop_size(public_key: int, subject: int = 7) -> int:
    """Determine how many loops of *subject* produce *public_key*."""
    value = 1
    loop = 0
    while value != public_key:
        value = (value * subject) % MODULO
        loop += 1
    return loop


def transform(subject: int, loop_size: int) -> int:
    """Transform *subject* by *loop_size* iterations."""
    value = 1
    for _ in range(loop_size):
        value = (value * subject) % MODULO
    return value


def find_encryption_key(card_public: int, door_public: int) -> int:
    """Derive the encryption key from the two public keys."""
    card_loop = find_loop_size(card_public)
    return transform(door_public, card_loop)


def solve(input_path: str = "advent2020/Day25/d25_input.txt") -> int:
    """Read the two public keys and return the encryption key."""
    lines = Path(input_path).read_text().strip().splitlines()
    card_public = int(lines[0])
    door_public = int(lines[1])
    return find_encryption_key(card_public, door_public)


if __name__ == "__main__":
    result = solve()
    print(f"Encryption key: {result}")
