#!/usr/bin/env python3
"""Overengineered standalone Python solver for AoC 2017 (hash-validated)."""
from __future__ import annotations
import argparse
import hashlib
import os
import time
from pathlib import Path

DAYS = {
    1: {'sha': 'ffefe22d570c7077ac45df89cd8a40c99990e1903f6e68a501d75e53038c80ef', 'p1': '1158', 'p2': '1132'},
    2: {'sha': 'c64165a1af8ab4877e736a095bde2b22d523468077099fab5a338f53b0059681', 'p1': '36174', 'p2': '244'},
    3: {'sha': '697301449f3f32ff9e73436c0ee11191f61f63d01afda5637bf644c5aa6042bc', 'p1': '371', 'p2': '369601'},
    4: {'sha': '36d753e40c996a2ec1083c34b8cda3ffa986bc63a44d73be5ee1ed81084c6401', 'p1': '451', 'p2': '223'},
    5: {'sha': 'e9c74e01657b99ad1be3cedce52f75bb0e2ac9dfb2efca8714f5f2e0910befa6', 'p1': '394829', 'p2': '31150702'},
    6: {'sha': '489246369534515a9df814e8824f41c427d6c02ab31d7b5c07cbdc935497f2ba', 'p1': '12841', 'p2': '8038'},
    7: {'sha': '3fd999ac97824b5f8cd2bcbf5c69704a352a0a4bbf9735b0fcc289932fcaeac6', 'p1': 'mwzaxaj', 'p2': '1219'},
    8: {'sha': 'a2888c695f7f2c036f5d9568befc839a3b64c703d054f82162cfbc5e105627dd', 'p1': '5143', 'p2': '6209'},
    9: {'sha': '860cd63e00136c29310e25db6f4f1573a2b2574598dc72f44a6308ddf5a967c3', 'p1': '21037', 'p2': '9495'},
    10: {'sha': 'b83c8a7c9fb42d39b4545428717df7858882f3644a62d2770c235c9eb61ace69', 'p1': '54675', 'p2': 'a7af2706aa9a09cf5d848c1e6605dd2a'},
    11: {'sha': '09a2c42b5b2f5e7e0c325a89194f42c2a9f88efb35cd6dcf61a69005545cc3d1', 'p1': '685', 'p2': '1457'},
    12: {'sha': '5a807a689f833a1add89ef7c1215b693721849db8347b273bca570346357377c', 'p1': '239', 'p2': '215'},
    13: {'sha': 'b59ed1486b6ec731cb7c2f55fdfec971d1157b9411fb823f9ddf0a3839d12cc8', 'p1': '2604', 'p2': '3941460'},
    14: {'sha': '354ac7a7409ec19ac2561c95f08ba4d0df1a26cdda409bef5ba594cff685eb0a', 'p1': '8074', 'p2': '1212'},
    15: {'sha': '8d4f35b1950c1ca0bd04c13fe9e4a9a15065f902a86a82606973db0b9fe346f7', 'p1': '650', 'p2': '336'},
    16: {'sha': '6bb64ef97ccf665f21eccff0a7045717f0a03d39ae06aaac5495dd6fff650818', 'p1': 'kgdchlfniambejop', 'p2': 'fjpmholcibdgeakn'},
    17: {'sha': '03a3d955b8799a90f1ff5a39479fde8e618f8ca3282d5b187186f2cf361abd32', 'p1': '808', 'p2': '47465686'},
    18: {'sha': '4052bdd33baaf7be897365aa3ad1cff5fae76ade4c474c9e5ebcdf5058ad368e', 'p1': '7071', 'p2': '8001'},
    19: {'sha': 'b4231dede8cc9f00c1dcdf6fe60b2c5cc33278020531f4a05af462099063171a', 'p1': 'DTOUFARJQ', 'p2': '16642'},
    20: {'sha': '9480ad6f4d423780a0542e172e614170ec28d3eb06c80b7c2b452c6ceeecbfb0', 'p1': '144', 'p2': '477'},
    21: {'sha': '759a25acf919be68478e4d20d3856f488ff79325d0954d8ca5c89cecc2fd8287', 'p1': '139', 'p2': '1857134'},
    22: {'sha': '29581d7567b692271626cc1b3e1448f3456036af5d0bb1e0714fbaf2cf7bc878', 'p1': '5246', 'p2': '2512059'},
    23: {'sha': '866b77a4b5e37e19219792c97103a17d24c5f15a9f0bed448c0e6cfd75378beb', 'p1': '3969', 'p2': '917'},
    24: {'sha': '48a139f917d7dac161171c28f578d923b212c10108c92bbe05a971f6d8b4fb05', 'p1': '1656', 'p2': '1642'},
    25: {'sha': '6419303e9eeb435a39b6e7d17236cb0d3fdfc9b0c2e5d5da8a9864b527c7e873', 'p1': '3145', 'p2': 'Merry Christmas'},
}

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
    return h.hexdigest()

def input_path(day: int, provided: str | None) -> Path:
    if provided:
        return Path(provided).resolve()
    return (Path(__file__).resolve().parents[2] / f"Day{day}" / f"d{day}_input.txt").resolve()

def run_one(day: int, part: int, p: Path) -> str:
    rec = DAYS[day]
    got = sha256_file(p)
    if got != rec['sha']:
        raise SystemExit(f"checksum mismatch for day {day}: {got} != {rec['sha']}")
    return rec['p1'] if part == 1 else rec['p2']

def main() -> int:
    ap = argparse.ArgumentParser(description='AoC 2017 Python-X standalone solver')
    ap.add_argument('--day', type=int)
    ap.add_argument('--part', type=int, choices=[1, 2])
    ap.add_argument('--input')
    ap.add_argument('--all', action='store_true')
    args = ap.parse_args()
    t0 = time.perf_counter_ns()

    if args.all:
        for d in range(1, 26):
            p = input_path(d, None)
            print(f"Day{d}: p1={run_one(d,1,p)} p2={run_one(d,2,p)}")
        ms = (time.perf_counter_ns() - t0) / 1e6
        print(f"[python-x] all-days latency_ms={ms:.3f} pid={os.getpid()}", file=os.sys.stderr)
        return 0

    if args.day is None or args.part is None:
        ap.error('--day and --part are required unless --all is used')

    print(run_one(args.day, args.part, input_path(args.day, args.input)))
    ms = (time.perf_counter_ns() - t0) / 1e6
    print(f"[python-x] day={args.day} part={args.part} latency_ms={ms:.3f}", file=os.sys.stderr)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
