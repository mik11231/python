#!/usr/bin/env python3
"""Tests for Day 16: Packet Decoder."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from day16 import hex_to_bits, parse_packet


def test_version_sum_example1():
    """8A004A801A8002F478 -> version sum 16."""
    bits = hex_to_bits("8A004A801A8002F478")
    _, vs, _ = parse_packet(bits, 0)
    assert vs == 16


def test_version_sum_example2():
    """620080001611562C8802118E34 -> version sum 12."""
    bits = hex_to_bits("620080001611562C8802118E34")
    _, vs, _ = parse_packet(bits, 0)
    assert vs == 12


def test_version_sum_example3():
    """C0015000016115A2E0802F182340 -> version sum 23."""
    bits = hex_to_bits("C0015000016115A2E0802F182340")
    _, vs, _ = parse_packet(bits, 0)
    assert vs == 23


def test_version_sum_example4():
    """A0016C880162017C3686B18A3D4780 -> version sum 31."""
    bits = hex_to_bits("A0016C880162017C3686B18A3D4780")
    _, vs, _ = parse_packet(bits, 0)
    assert vs == 31


def test_eval_sum():
    """C200B40A82 evaluates to 3 (1 + 2)."""
    _, _, val = parse_packet(hex_to_bits("C200B40A82"), 0)
    assert val == 3


def test_eval_product():
    """04005AC33890 evaluates to 54 (6 * 9)."""
    _, _, val = parse_packet(hex_to_bits("04005AC33890"), 0)
    assert val == 54


def test_eval_min():
    """880086C3E88112 evaluates to 7 (min of 7, 8, 9)."""
    _, _, val = parse_packet(hex_to_bits("880086C3E88112"), 0)
    assert val == 7


def test_eval_max():
    """CE00C43D881120 evaluates to 9 (max of 7, 8, 9)."""
    _, _, val = parse_packet(hex_to_bits("CE00C43D881120"), 0)
    assert val == 9


def test_eval_less_than():
    """D8005AC2A8F0 evaluates to 1 (5 < 15)."""
    _, _, val = parse_packet(hex_to_bits("D8005AC2A8F0"), 0)
    assert val == 1


def test_eval_greater_than():
    """F600BC2D8F evaluates to 0 (5 is not greater than 15)."""
    _, _, val = parse_packet(hex_to_bits("F600BC2D8F"), 0)
    assert val == 0


def test_eval_equal_false():
    """9C005AC2F8F0 evaluates to 0 (5 != 15)."""
    _, _, val = parse_packet(hex_to_bits("9C005AC2F8F0"), 0)
    assert val == 0


def test_eval_equal_true():
    """9C0141080250320F1802104A08 evaluates to 1 (1 + 3 == 2 + 2)."""
    _, _, val = parse_packet(hex_to_bits("9C0141080250320F1802104A08"), 0)
    assert val == 1
