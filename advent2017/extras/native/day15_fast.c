#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

static const uint64_t FA = 16807ULL;
static const uint64_t FB = 48271ULL;
static const uint64_t MOD = 2147483647ULL;
static const uint64_t MASK = 0xFFFFULL;

static uint64_t solve_part1(uint64_t a, uint64_t b) {
    uint64_t cnt = 0;
    for (uint32_t i = 0; i < 40000000U; ++i) {
        a = (a * FA) % MOD;
        b = (b * FB) % MOD;
        cnt += ((a & MASK) == (b & MASK));
    }
    return cnt;
}

static uint64_t solve_part2(uint64_t a, uint64_t b) {
    uint64_t cnt = 0;
    for (uint32_t i = 0; i < 5000000U; ++i) {
        do { a = (a * FA) % MOD; } while ((a & 3ULL) != 0ULL);
        do { b = (b * FB) % MOD; } while ((b & 7ULL) != 0ULL);
        cnt += ((a & MASK) == (b & MASK));
    }
    return cnt;
}

int main(int argc, char** argv) {
    if (argc != 4) {
        fprintf(stderr, "usage: %s <part> <a_seed> <b_seed>\n", argv[0]);
        return 2;
    }
    int part = atoi(argv[1]);
    uint64_t a = (uint64_t)strtoull(argv[2], NULL, 10);
    uint64_t b = (uint64_t)strtoull(argv[3], NULL, 10);
    uint64_t ans = 0;
    if (part == 1) ans = solve_part1(a, b);
    else if (part == 2) ans = solve_part2(a, b);
    else return 3;
    printf("%llu\n", (unsigned long long)ans);
    return 0;
}
